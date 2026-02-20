# Maton API 集成中间层详解

> 创建时间：2026-02-19  
> 标签：#Maton #API #Stripe #集成 #OAuth

---

## 📌 什么是 Maton？

**Maton** 是一个 **API 集成中间层服务**，用于简化第三方 API（如 Stripe、Slack 等）的认证和访问。

**官方网站：** [https://maton.ai](https://maton.ai)

---

## 🎯 Maton 的核心作用

### 1️⃣ OAuth 认证代理

```
用户 → Maton → 第三方 API (如 Stripe)
      ↑
   OAuth 管理
```

**没有 Maton 时：**
- ❌ 需要直接向第三方注册应用
- ❌ 管理 Client ID / Client Secret
- ❌ 处理 OAuth 回调
- ❌ 管理 Refresh Token
- ❌ 处理 Token 过期刷新

**有 Maton 后：**
- ✅ 只需一个 Maton API Key
- ✅ Maton 处理所有 OAuth 流程
- ✅ Token 自动刷新
- ✅ 只需调用 Maton 的 API

---

### 2️⃣ API 网关/代理

```
你的请求
  ↓
https://gateway.maton.ai/stripe/v1/customers
  ↓
Maton 自动添加第三方 API Key
  ↓
https://api.stripe.com/v1/customers
```

**你不需要：**
- ❌ 存储第三方 API Key
- ❌ 在代码中处理敏感凭证
- ❌ 担心 Key 泄露

**Maton 帮你：**
- ✅ 安全存储凭证
- ✅ 自动注入认证头
- ✅ 统一管理多个账号

---

### 3️⃣ 多账号连接管理

```bash
# 可以连接多个同类型账号
Connection A → 公司 Stripe 账号
Connection B → 个人 Stripe 账号
Connection C → 测试 Stripe 账号

# 使用时指定连接
curl -H "Maton-Connection: {connection_id}" ...
```

---

## 📊 架构对比

### 传统方式（直接调用第三方 API）

```
┌─────────────┐
│   你的代码   │
└──────┬──────┘
       │ 直接管理
       ↓
┌─────────────────┐
│ 第三方 API Key  │ ← 敏感信息，需要安全存储
└──────┬──────────┘
       │
       ↓
┌─────────────┐
│ 第三方 API  │
└─────────────┘
```

### 使用 Maton 的方式

```
┌─────────────┐
│   你的代码   │
└──────┬──────┘
       │ 只需 Maton API Key
       ↓
┌─────────────┐
│    Maton    │ ← 管理 OAuth、Token 刷新
└──────┬──────┘
       │ 自动注入第三方凭证
       ↓
┌─────────────┐
│ 第三方 API  │
└─────────────┘
```

---

## ✅ Maton 的优势

| 功能 | 直接调用 | 使用 Maton |
|------|---------|-----------|
| **认证管理** | 自己处理 OAuth | Maton 托管 |
| **Token 刷新** | 手动处理 | 自动刷新 |
| **多账号** | 复杂 | 简单切换 |
| **安全性** | 自己保护 Key | Maton 保护 |
| **调试** | 直接看日志 | Maton 控制台 |
| **代码复杂度** | 高 | 低 |

---

## ⚠️ 潜在缺点

| 问题 | 说明 |
|------|------|
| **依赖第三方** | Maton 服务挂了就无法访问下游 API |
| **额外延迟** | 请求多了一跳代理，增加少量延迟 |
| **隐私考虑** | 你的 API 数据经过 Maton 服务器 |
| **成本** | 目前免费，但未来可能收费 |
| **功能限制** | 依赖 Maton 支持的 API 范围 |

---

## 🔧 快速开始

### 1. 注册账号

访问 [https://maton.ai](https://maton.ai) 注册账号

### 2. 获取 API Key

1. 登录 [maton.ai](https://maton.ai)
2. 前往 [maton.ai/settings](https://maton.ai/settings)
3. 复制你的 API Key

### 3. 设置环境变量

```bash
# 临时设置（当前终端会话）
export MATON_API_KEY="YOUR_API_KEY"

# 永久设置（添加到 ~/.zshrc）
echo 'export MATON_API_KEY="YOUR_API_KEY"' >> ~/.zshrc
source ~/.zshrc
```

### 4. 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'stripe'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 5. 完成 OAuth 授权

打开返回的 `url` 在浏览器中，登录第三方账号并完成授权。

---

## 🔗 核心 API 端点

### 连接管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/connections` | GET | 列出所有连接 |
| `/connections` | POST | 创建新连接 |
| `/connections/{id}` | GET | 获取连接详情 |
| `/connections/{id}` | DELETE | 删除连接 |

### API 网关

```
https://gateway.maton.ai/{app}/{api-path}
```

**示例：**
```bash
# Stripe API
https://gateway.maton.ai/stripe/v1/customers

# 其他支持的 API
https://gateway.maton.ai/{app}/v1/{resource}
```

---

## 💡 使用示例（以 Stripe 为例）

### 查询客户列表

```bash
curl -g "https://gateway.maton.ai/stripe/v1/customers?limit=10" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq .
```

### 创建客户

```bash
curl -g -X POST "https://gateway.maton.ai/stripe/v1/customers" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=customer@example.com&name=John Doe"
```

### 查询余额

```bash
curl -g "https://gateway.maton.ai/stripe/v1/balance" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq .
```

### 指定连接（多账号场景）

```bash
curl -g "https://gateway.maton.ai/stripe/v1/customers" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Maton-Connection: c3c82a73-4c86-4c73-8ebd-1f325212fde6"
```

---

## 🔐 安全考虑

### Maton 的安全机制

| 机制 | 说明 |
|------|------|
| **API Key 认证** | 所有请求需要 Maton API Key |
| **OAuth 托管** | 第三方凭证由 Maton 安全存储 |
| **连接隔离** | 每个连接有独立 ID |
| **HTTPS** | 所有通信加密 |

### 你自己的安全措施

```bash
# 1. 不要将 API Key 提交到 Git
echo "MATON_API_KEY" >> .gitignore

# 2. 使用环境变量
export MATON_API_KEY="your_key"

# 3. 定期轮换 Key
# 在 maton.ai/settings 重新生成

# 4. 限制连接权限
# 在 Maton 控制台设置连接范围
```

---

## 🛠️ 故障排查

### 问题 1: 401 未授权

```bash
# 检查 API Key 是否设置
echo $MATON_API_KEY

# 测试连接
curl "https://ctrl.maton.ai/connections" \
  -H "Authorization: Bearer $MATON_API_KEY"

# 如果返回 401，检查：
# 1. API Key 是否正确
# 2. API Key 是否过期
# 3. 是否有前缀 "Bearer "
```

### 问题 2: 404 未找到

```bash
# 确保 URL 路径正确
# 正确：/stripe/v1/customers
# 错误：/v1/customers

# 检查 app 名称是否正确
curl "https://gateway.maton.ai/stripe/v1/customers"
```

### 问题 3: 连接失效

```bash
# 检查连接状态
curl "https://ctrl.maton.ai/connections?app=stripe&status=ACTIVE"

# 如果连接不存在，重新创建
# 如果状态不是 ACTIVE，重新授权
```

---

## 📋 支持的第三方服务

Maton 支持多种第三方 API 集成，包括但不限于：

| 服务 | 类型 | 状态 |
|------|------|------|
| Stripe | 支付 | ✅ 支持 |
| Slack | 通讯 | ✅ 支持 |
| Google | 认证 | ✅ 支持 |
| ... | ... | 📝 查看官网 |

**查看完整列表：** [https://maton.ai](https://maton.ai)

---

## 🎯 使用场景

### 适合使用 Maton 的场景

| 场景 | 说明 |
|------|------|
| **快速原型** | 不想花时间处理 OAuth |
| **多账号管理** | 需要切换多个第三方账号 |
| **安全性要求高** | 不想在代码中存储敏感 Key |
| **团队协作** | 统一管理团队凭证 |
| **学习/测试** | 快速测试第三方 API |

### 不适合使用 Maton 的场景

| 场景 | 说明 |
|------|------|
| **高并发生产** | 额外延迟可能影响性能 |
| **数据隐私敏感** | 不想数据经过第三方 |
| **成本敏感** | 未来可能收费 |
| **特殊定制需求** | Maton 不支持的 API |

---

## 🔗 相关资源

| 资源 | 链接 |
|------|------|
| **Maton 官网** | https://maton.ai |
| **Maton 设置** | https://maton.ai/settings |
| **连接管理** | https://ctrl.maton.ai |
| **Maton 社区** | https://discord.com/invite/dBfFAcefs2 |
| **支持邮箱** | support@maton.ai |
| **Stripe API** | https://docs.stripe.com/api |

---

## 💭 类比理解

```
Maton 之于第三方 API ≈ 支付宝 之于 银行

你想付款 → 不用直接操作银行账户 → 用支付宝就行
你想调 API → 不用直接管理 API Key → 用 Maton 就行
```

或者：

```
Maton ≈ API 界的"密码管理器"

1Password 存储你的登录密码
Maton 存储你的 API 凭证

你用主密码访问 1Password
你用 Maton API Key 访问第三方 API
```

---

## 📝 更新日志

- **2026-02-19**: 初始版本，整理 Maton 核心概念和使用指南
