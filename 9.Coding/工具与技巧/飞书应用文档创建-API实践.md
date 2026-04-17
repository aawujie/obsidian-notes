# 飞书应用文档创建 — API 实践

> 飞书自建应用通过 Open API 创建云文档、写入结构化内容、设置分享权限的完整方案。
> 核心发现：**应用只能在自己的空间创建文档，无法直接写入用户的 Wiki 或文件夹**。

## 背景

需求：`auto_diagnosis` 每次生成 AI 诊断报告后，自动创建飞书文档并将链接发送到群聊，取代直接在消息中贴长文本。

## 权限模型（踩坑重点）

### 应用权限 vs 资源权限

飞书的权限分两层：

| 层级 | 含义 | 举例 |
|---|---|---|
| **API Scope** | 应用能调用哪些 API | `docx:document`、`drive:drive`、`wiki:wiki` |
| **资源协作者** | 应用对具体资源（文件夹/文档/Wiki）的访问权 | 文件夹管理员、文档可编辑 |

即使 API Scope 全开，应用也**无法访问**用户的私人文件夹或 Wiki（除非被加为协作者）。

### 解决方案：应用自建文件夹

应用首次创建文档时，飞书会自动为它创建一个「应用文件夹」（在 Drive 根目录）。可以指定 `folder_token` 让文档归入该文件夹。

**关键限制**：
- 用户的文件夹 → 不能通过 API 把应用加为协作者（UI 中「添加协作者」也搜不到应用）
- Wiki 空间 → 需要空间管理员手动添加应用为成员
- 应用自己的文件夹 → 用户默认看不到，但可以通过**文档级权限**解决

### 最终方案

```
应用创建文档 → 写入内容 → 设置文档权限为"组织内可查看" → 发送链接
```

不需要用户能看到文件夹，只要能通过链接打开文档即可。

## API 调用流程

### 1. 获取 tenant_access_token

```
POST /open-apis/auth/v3/tenant_access_token/internal
Body: { "app_id": "...", "app_secret": "..." }
```

返回 `tenant_access_token`，有效期 2 小时。

### 2. 创建文档

```
POST /open-apis/docx/v1/documents
Headers: Authorization: Bearer {token}
Body: {
    "folder_token": "PBjhfvEF8l0SDsdVCjzcX8rCnJg",  // 应用自建文件夹
    "title": "[诊断报告] HIL 2026-03-26"
}
```

返回 `document_id`，后续用于写入内容和设置权限。

### 3. 写入结构化内容

```
POST /open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children
Body: { "children": [...blocks], "index": 0 }
```

#### block_type 速查

| block_type | 类型 | 字段名 |
|---|---|---|
| 2 | 普通文本 | `text` |
| 3 | heading1 | `heading1` |
| 4 | heading2 | `heading2` |
| 5 | heading3 | `heading3` |
| 14 | 代码块 | `code` |
| 12 | 有序列表 | `ordered` |
| 13 | 无序列表 | `bullet` |

每个 block 的文本内容都通过 `elements` 数组传入：

```json
{
    "block_type": 4,
    "heading2": {
        "elements": [{"text_run": {"content": "概览"}}]
    }
}
```

代码块需要额外指定语言：

```json
{
    "block_type": 14,
    "code": {
        "elements": [{"text_run": {"content": "错误日志内容..."}}],
        "style": {"language": 1}
    }
}
```

**注意**：heading 类型的 block **不要**传 `style` 字段，否则会报 `invalid param`。

### 4. 设置文档权限

```
PATCH /open-apis/drive/v1/permissions/{doc_id}/public?type=docx
Body: {
    "external_access_entity": "closed",
    "security_entity": "anyone_can_view",
    "link_share_entity": "tenant_readable"
}
```

设置后，组织内任何人通过链接即可查看文档。

### 所需 API Scope

| Scope | 用途 |
|---|---|
| `docx:document` | 创建/写入文档 |
| `drive:drive` | 文件夹操作、权限设置 |

## SSL 注意事项

在某些环境下（如公司内网代理），Python `urllib` 调用飞书 API 可能遇到 SSL 证书验证失败。解决方法：

```python
import ssl
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE
# 传给 urlopen
urllib.request.urlopen(req, timeout=15, context=_SSL_CTX)
```

## 使用的飞书应用

- App ID: `cli_a8ebffa9f939900e`
- 环境变量: `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- 文件夹 Token: `PBjhfvEF8l0SDsdVCjzcX8rCnJg`（应用自建的 `HIL_诊断报告` 文件夹）

## 踩坑记录

1. **Wiki 权限墙**：即使应用有 `wiki:wiki` scope，也需要 Wiki 空间管理员手动添加应用为空间成员，否则 `permission denied: node permission denied`
2. **用户文件夹不可写**：应用无法通过 API 将自己加为用户文件夹的协作者
3. **block_type 枚举**：飞书文档 API 的 block_type 是数字不是字符串，heading2 是 4 不是 `"heading2"`
4. **heading 不要传 style**：heading 类型 block 传空 `style: {}` 会导致 `invalid param`
5. **权限类型参数**：`/permissions/{id}/public` 必须带 `?type=docx`，不带或传 `folder` 会 400
6. **security_entity 取值**：`anyone_can_view` 表示"有链接可查看"，不是 `tenant_readable`（后者用于 `link_share_entity`）
