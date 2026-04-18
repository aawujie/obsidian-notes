---
notion-id: 2a078d23-e296-8017-b319-ef6801f36fc7
Last edited time: 2025-12-12T16:24:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
## 引言

本笔记聚焦加密货币（Cryptocurrency）和区块链（Blockchain）领域中与**加密库（Cryptographic Libraries）**相关的技术标准与安全缩写。这些缩写主要涉及密钥生成、哈希函数、签名算法和协议改进，常用于开发钱包、智能合约或区块链工具（如 Python 的 `hashlib`、`hmac`、`ecdsa` 库）。我从核心 BIP 标准、哈希/认证机制和签名/地址格式入手，精选约 15 个高频缩写。每个条目包括全称、简要解释、加密库关联及示例用法。

笔记基于 BIP 官网和标准 RFC（如 RFC 2104 for HMAC），适用于开发者参考。实践建议：用 Python 的 `ecdsa` 库实现 ECDSA 签名，或 `hashlib` 复现 PBKDF2。

---

## 技术标准缩写（BIP & 协议）

这些是比特币/以太坊的核心改进提案，常直接影响加密库实现。

| 缩写 | 全称 | 解释 | 加密库关联 | 示例 |
| --- | --- | --- | --- | --- |
| BIP | Bitcoin Improvement Proposal | 比特币改进提案，用于标准化协议变更，如密钥派生和地址格式。 | 库如 `bip-utils` (Python) 实现 BIP 解析。 | "BIP44 定义多币种 HD 路径 m/44'/coin'/account'/change/index。" |
| BIP32 | Bitcoin Improvement Proposal 32 | 层级确定性（HD）钱包标准，从单一种子生成树状密钥对，确保备份一致性。 | 使用 `hmac` + `hashlib` 实现 CKD (Child Key Derivation) 函数。 | "BIP32 用 HMAC-SHA512 从主种子衍生子私钥。" |
| BIP39 | Bitcoin Improvement Proposal 39 | 助记词标准，将 128-256 位熵转换为 12-24 词短语，用于用户友好备份。 | `mnemonic` 库生成/验证助记词，结合 PBKDF2 派生种子。 | "BIP39 测试种子 'abandon abandon...' 生成固定种子。" |
| BIP44 | Bitcoin Improvement Proposal 44 | 多账户 HD 钱包路径标准，支持多币种衍生（如 m/44'/0'/0'/0/0 为 BTC 第一个地址）。 | 集成到 `pycoin` 或 `bitcoinlib` 库中路径解析。 | "BIP44 路径用于 Electrum 钱包地址生成。" |
| SLIP-44 | Standards for Layered Independent Primitives 44 | 币种特定 HD 路径注册表，扩展 BIP44 到其他链。 | 库查询 SLIP-44 注册以获取 coin_type（如 ETH 为 60）。 | "SLIP-44 为 SOL (Solana) 指定路径 m/44'/501/0'/0'。" |

---

## 安全与哈希机制缩写

这些是底层加密原语，常在库中作为构建块，用于认证和派生。

| 缩写 | 全称 | 解释 | 加密库关联 | 示例 |
| --- | --- | --- | --- | --- |
| HMAC | Hash-based Message Authentication Code | 基于哈希的消息认证码，使用密钥验证消息完整性，防篡改。 | Python `hmac` 模块：`hmac.new(key, msg, hashlib.sha512)`。 | "BIP32 CKD 用 HMAC-SHA512 衍生子密钥，输出 512 位 IL/Chain Code。" |
| PBKDF2 | Password-Based Key Derivation Function 2 | 密码基密钥派生函数，通过迭代哈希（如 2048 次）从弱密码生成强密钥。 | `hashlib.pbkdf2_hmac('sha512', mnemonic, salt, iterations)`。 | "BIP39 用 PBKDF2 从助记词 + 'mnemonic' 盐生成 512 位种子。" |
| SHA-256 | Secure Hash Algorithm 256 | 产生 256 位摘要的哈希函数，用于交易 ID 和地址校验。 | `hashlib.sha256(data).digest()`，比特币核心依赖。 | "比特币区块哈希 = SHA-256(SHA-256(header))。" |
| SHA-512 | Secure Hash Algorithm 512 | 产生 512 位摘要的哈希函数，用于密钥衍生而非交易。 | `hashlib.sha512()` 在 HMAC 中常见。 | "BIP32 主密钥 = HMAC-SHA512('Bitcoin seed', seed)[:32]。" |
| RIPEMD-160 | RACE Integrity Primitives Evaluation Message Digest 160 | 产生 160 位哈希的函数，常与 SHA-256 结合用于地址压缩。 | `hashlib.new('ripemd160', sha256_pubkey).digest()`。 | "P2PKH 地址哈希 = RIPEMD-160(SHA-256(公钥))。" |

---

## 签名与地址格式缩写

这些涉及椭圆曲线和支付脚本，用于交易验证和地址生成。

| 缩写 | 全称 | 解释 | 加密库关联 | 示例 |
| --- | --- | --- | --- | --- |
| ECDSA | Elliptic Curve Digital Signature Algorithm | 椭圆曲线数字签名算法，提供高效公私钥签名，用于证明所有权。 | Python `ecdsa` 库：`SigningKey.from_string(privkey, curve=SECP256k1)`。 | "比特币交易签名 = ECDSA(私钥, 交易哈希)。" |
| secp256k1 | Secure Elliptic Curve over Prime Field 256 bits Key | 比特币专用的椭圆曲线，提供 256 位安全性，用于密钥生成。 | `ecdsa.SECP256k1` 曲线参数。 | "公钥 = secp256k1 乘法(生成点, 私钥)。" |
| P2PKH | Pay-to-Public-Key-Hash | 传统比特币地址脚本（OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG）。 | 库如 `bitcoin` 生成：版本 + pubkey_hash + checksum。 | "地址 '1BgGZ9tc...' = Base58(0x00 + RIPEMD160(SHA256(公钥)) + CSUM)。" |
| P2SH | Pay-to-Script-Hash | 支付到脚本哈希，支持多签名或复杂脚本（以 '3' 开头）。 | 哈希 redeemScript：RIPEMD160(SHA256(script))。 | "P2SH 用于 2-of-3 多签钱包。" |
| HD | Hierarchical Deterministic Wallet | 层级确定性钱包，从根种子确定性生成所有密钥。 | 结合 BIP32/39，在 `trezor` 或 `ledger` 库中实现。 | "HD 路径 m/0' 为硬化衍生，增强隐私。" |

---

## 学习提示

- **实践代码**：用 Python 复现 BIP39/BIP32（如前对话），导入 `ecdsa` 生成真实公钥（非占位 SHA256）。
- **库推荐**：Python - `ecdsa` (签名)、`hashlib/hmac` (哈希)、`bip-utils` (BIP 工具)；JS - `ethers.js` (ETH 集成)。
- **扩展**：若需更多如 AES (对称加密，非核心) 或 Schnorr (Taproot 签名)，参考 BIP 341。定期查 GitHub 仓库如 bitcoin/bips。

这份精简笔记便于开发者快速查阅。如果你想添加代码示例或特定库集成，告诉我！