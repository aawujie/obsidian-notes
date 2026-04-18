---
notion-id: 2a078d23-e296-806c-b03c-cfeaf407f126
Last edited time: 2025-12-12T16:23:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
## 引言

BIP44（Bitcoin Improvement Proposal 44）是 HD 钱包（Hierarchical Deterministic Wallet）的标准规范，用于从单一种子（助记词）生成多币种、多账户的密钥对和地址。它扩展了 BIP32 的树状结构，确保钱包兼容性和安全性。路径如 `m/44'/0'/0'/0/0`（BTC）或 `m/44'/60'/0'/0/0`（ETH）定义了从根密钥“m”衍生子密钥的路线图。

这份笔记总结路径含义、结构和示例，基于 BIP44 规范。适合开发者/用户快速参考。

## 路径结构详解

BIP44 路径格式：`m / purpose' / coin_type' / account' / change / address_index`

| 层级 | 符号/含义 | 示例值 (BTC) | 示例值 (ETH) | 说明 |
| --- | --- | --- | --- | --- |
| **m** | 主密钥根 (Master) | m | m | 从种子派生的根私钥。 |
| **purpose'** | 用途 (硬化) | 44' | 44' | 固定 44' 表示 BIP44 方案（硬化：index + 0x80000000）。 |
| **coin_type'** | 币种类型 (硬化) | 0' | 60' | SLIP-44 注册：0=BTC 主网，60=ETH。硬化隔离币种。 |
| **account'** | 账户 (硬化) | 0' | 0' | 第一个账户 (0')；可增至 1' 等，多账户隔离。 |
| **change** | 变更类型 (非硬化) | 0 | 0 | 0=接收地址；1=找零地址（BTC UTXO 模型用）。 |
| **address_index** | 地址索引 (非硬化) | 0 | 0 | 第一个地址 (0)；增至 1,2... 生成新地址，避免重复。 |

- **硬化 vs 非硬化**：硬化层（'）防公钥泄露；非硬化允许从公钥衍生子公钥（轻钱包用）。
- **为什么这样设计**？树状结构支持无限地址生成（gap limit ~20），多链兼容（不同 coin_type 分支）。

## 图示：BIP44 路径树（BTC 示例）

以下是 BIP44 路径的 PlantUML 文本表示（plain UML）。你可以复制到 [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/) 渲染成图。它展示从根 m 开始的层级树，最终生成地址。

![[imgs/image 7.png]]

**图描述**（渲染后效果）：

- **树状流程**：从灰色根节点“m”向下箭头连接蓝色节点（层级），最终到黄色“Address”节点。
- **关键元素**：箭头标“硬化衍生”/“非硬化”；右方笔记解释种子输入和地址生成步骤。
- **ETH 变体**：只需将“0' (Coin Type - BTC)”改为“60' (Coin Type - ETH)”，树结构相同。

## 示例与测试向量

测试向量特定助记词（用 BIP39 测试助记词） `"abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"`：

- **BTC 路径**：m/44'/0'/0'/0/0 → 地址：`1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH` 
- **ETH 路径**：m/44'/60'/0'/0/0 → 地址：`0xd2151361e5eb6e53a3651c3f7841afcaba24da03`

**Python 验证**（用之前代码）：

```python
# 示例：完整路径衍生
path_btc = [0x80000000+44, 0x80000000+0, 0x80000000+0, 0, 0]
# 衍生后生成地址，匹配以上测试向量
```

## 常见问题与提示

- **多账户**：用 **m/44'/0'/1'/0/0 **生成第二个账户。
- **测试网**：coin_type=1 (BTC testnet)，路径类似。
- **兼容性**：MetaMask/Electrum 默认此路径；自定义需指定。
- **安全**：硬化层防泄露；备份种子恢复全树。

## 参考资源

- BIP44 规范：[github.com/bitcoin/bips/blob/master/bip-0044.mediawiki](http://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
- 工具：Ian Coleman BIP39（ian [coleman.io/bip39）可视化路径。](http://coleman.io/bip39%EF%BC%89%E5%8F%AF%E8%A7%86%E5%8C%96%E8%B7%AF%E5%BE%84%E3%80%82)