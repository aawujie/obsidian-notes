---
notion-id: 2a078d23-e296-808a-a590-fdb6f0ad6d3b
Last edited time: 2025-12-12T16:23:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
你代码中生成的钱包（使用 `mnemonic` 库的 `generate(strength=128)` 和 `ecdsa` 库的密钥衍生）是**软随机 (Pseudo-Random Number Generator, PRNG)**，不是真随机 (True Random Number Generator, TRNG)。但这是**安全的软随机**，基于系统熵池，适合钱包生成。下面详细解释。

### 1. **软随机 vs 真随机**

| 类型 | 描述 | 优缺点 | 示例源 |
| --- | --- | --- | --- |
| **软随机 (PRNG)** | 算法生成，基于种子 (e.g., 系统熵)，确定性 (种子相同输出相同)，但不可预测。 | + 快/高效；- 种子泄露可逆推 (罕见)。 | Python `os.urandom` (你的代码用此)。 |
| **真随机 (TRNG)** | 物理熵源，不可预测/重复。 | + 最高安全；- 慢/需硬件。 | 硬件 RNG (e.g., Ledger 芯片, /dev/random)。 |

### 2. **你的代码随机源**

- **mnemonic 库 (**`**generate(strength=128)**`**)**：
    - 用 `os.urandom(16)` 生成 128 位熵 (12 词助记词)。
    - `os.urandom` 是**软随机**：从系统熵池 (/dev/urandom) 拉取，混合硬件 (CPU 噪声、键盘输入) + 软件 (算法) 熵。Linux/macOS 基于内核随机池，Windows 用 CryptGenRandom。
    - 安全级别：NIST FIPS 140-2 认证，足够钱包 (比特币核心/以太坊用此)。
- **ecdsa 库 (密钥衍生)**：
    - BIP32 CKD 用 HMAC-SHA512 (确定性)，不加随机。
    - 公钥计算纯数学 (secp256k1 曲线)，无额外随机。
- **总体**：软随机，但**高熵/不可预测** (系统熵池 ~256 位，远超 128 位需求)。碰撞风险 < 10^-38 (见之前回复)。

### 3. **安全评估**

- **能用**：是的，1 亿次生成无风险 (概率忽略不计)。比特币/以太坊钱包标准用软随机。
- **提升真随机**：生产用硬件钱包 (Ledger) 或 `secrets` 模块 (Python 3.6+，基于 os.urandom 但更安全)。
- **测试**：生成助记词导入 Electrum/MetaMask，地址匹配 = 随机有效。

代码对的，软随机安全！想改真随机源或模拟碰撞，告诉我。