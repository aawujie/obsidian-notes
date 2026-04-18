---
notion-id: 25678d23-e296-81a8-983b-dd457e4a9228
cover: "[[imgs/EVM内部结构与执行流程详解.jpeg]]"
Date: 2025-08-22
Last edited time: 2025-08-23T22:13:00
Tags:
  - 执行力
  - 高效人生
  - 年入百万策略
Link: https://youtu.be/O8pImV1eRTE?si=remb0M5COVPQcOBX
pic: https://img.youtube.com/vi/O8pImV1eRTE/sddefault.jpg
Verification: unverified
Owner:
  - AI generation
---
# 1. Metadata

- Title: EVM 解剖：栈、内存、存储、字节码、操作码与合约执行流程（视频阅读版）
- Author: John Becker（Chainalysis 软件工程师，Heimdall 工具箱贡献者）

# 2. Overview

这段视频核心在于从底层角度讲解以太坊虚拟机（EVM）的内部结构与执行机制，覆盖 EVM 的“可变机械状态”（machine state）、字节码（bytecode）、操作码（opcodes）、栈（stack）、内存（memory）、存储（storage）、calldata（调用数据）、函数选择子（selector）以及合约执行的控制流图（control flow graph）。结论性要点包括：理解 EVM 需要把握栈式 VM 的基本规则（256 位字、最大栈深度、前 16 个可直接访问的栈元素等）、字节码如何被反汇编为操作码用于分析、如何从 calldata 的前 4 字节（selector）识别函数、操作码集合如何组成合约逻辑（包括 call、delegatecall、create/create2、log/selfdestruct 等）、Solidity 在 EVM 内部如何表示各类类型（address、uint、mapping、动态类型等），以及以 Heimdall、evm.codes、etherscan/etherface、Foundry 等工具作为分析与反编译的实践路径。

# 3. 按照主题来梳理

## 3.1 EVM 基本构件：栈、内存、存储、calldata、机器状态与字节码

- EVM（Ethereum Virtual Machine）是一个栈式虚拟机（stack-based virtual machine），其“字大小”（word size）为 256 位（即每个栈槽/内存/存储单元以 32 字节表示）。这个 256 位的限制意味着所有能直接处理的数值上限接近 2^256。实际上的含义是：每次操作（算术、逻辑、位运算）通常以 32 字节为单元来读写或计算。
- 机器状态（machine state）：视频里提到的“volatile machine state”（易失性机器状态）指的是那些只在单次交易执行期间存在的状态：栈（stack）、内存（memory）、程序计数器（program counter, PC）、剩余 gas 等。它们在交易执行结束或 revert 后不会持久化到链上。
- 字节码（bytecode）：合约部署到链上的就是字节码，它通常是不可修改的（不过可以通过 self-destruct 或代理模式达到变更行为的效果），字节码由编译器（如 Solidity）生成，然后存储在区块链的账户信息中。字节码以十六进制表示，反汇编后可以得到操作码（opcodes）的可读形式（例如 0x60 表示 PUSH1）。
- 栈（stack）：EVM 是后进先出（LIFO）的栈机。栈最多允许 1024（通常说 1,024，但视频中提到的是 1,24——应理解为 1024 的语音或笔误）深度（实际 EVM 限制为 1024），但只能直接通过 DUP/SWAP 系列操作访问顶部最多 16 个元素（dup1..dup16、swap1..swap16）。这是 Solidity 中出现 “stack too deep” 错误的主要根源。栈中每个元素是 32 字节长。
- 内存（memory）：内存是按需扩展的线性字节数组（byte array），只在单次交易执行过程中存在（易失性），不会持久化到链上。Solidity 将字符串、bytes、函数的返回数据等较长或动态的数据存放或编码在内存里。实现上可以把内存想象成一串 u8 向量（如 Rust 中 Vec），内存读写通过 MLOAD（读取 32 字节）、MSTORE（写入 32 字节）、MSTORE8（写入 1 字节）、MSIZE（当前内存大小）等操作码完成。
- 存储（storage）：与内存相对，storage 是持久化到链上的键值映射（类似 HashMap）。每个合约账户在链上有独立的 storage 空间，以 32 字节为单位的槽（slot）保存数据。常见用途包括 ERC-20 的余额映射（balances）、NFT 的 owner 映射、合约的名称/符号/所有者等。Solidity 在编译时会将高级类型映射为 storage 布局（例如简单变量固定存储槽、mapping 的键值通过 keccak256(hash) 形成槽地址、动态数组/字符串使用 RLP / offset 编码等）。
- calldata（调用数据）：calldata 是发送给合约函数的输入数据，它随交易一起被传入 EVM。calldata 的第一个 4 字节通常是函数选择子（selector），即 keccak256("functionName(type1,type2,...)") 的前 4 字节，用来标识要调用的具体函数。剩余部分按 ABI 编码，依次是参数值（固定长度按 32 字节对齐，动态类型放在内存/offset 位置并使用长度前缀等）。
- 函数选择子与反解码：只知道原始 calldata 时，可以用函数选择子来确定调用的函数。通过将 calldata 的前 4 字节与已知签名库（如 etherface / 4byte.directory）匹配，可以推断出函数签名。Heimdall 等工具会利用这些数据库配合字节码的控制流分析来推断 ABI，即便合约未发布源代码也能解出函数名与参数格式（不过存在歧义或冲突时需谨慎）。
- 小结：理解 EVM 的第一步是区分“临时状态”（栈/内存/PC/剩余 gas）和“持久状态”（storage/合约代码），理解 calldata 的结构与 selector 的作用，以及字节码如何映射到操作码以驱动执行。

## 3.2 操作码详解（opcodes）：分类、常用行为与实战意义

- 操作码的基本概念：字节码可以反汇编成一系列操作码（opcodes），每个 opcode 附带零个或多个立即数（例如 PUSH1 后面跟 1 字节常量, PUSH32 后面跟 32 字节）。左侧通常用程序计数器（PC）标注序号，用以指示下一条将要执行的指令。操作码执行会读写栈、内存或存储，或改变控制流（JUMP/JUMPI）或进行外部调用（CALL/DELEGATECALL/CALLCODE）等。
- 停止与异常：
    - STOP：立即停止执行，不返回数据。
    - INVALID：无效操作码，通常会消耗全部 gas 并导致异常终止（有时用于故意消耗 gas）。
    - REVERT：回滚并返回指定内存区的错误数据，状态回到调用前（但不消耗所有 gas，剩余 gas 会返回调用者）。
- 算术与比较运算：
    - ADD, MUL, SUB, DIV, SDIV（有符号除法）, MOD, SMOD（有符号取模）等用于对栈顶的 32 字节单元进行数学运算。
    - EXP（指数）、ADDMOD、MULMOD（带模加乘的优化版本）等用于特定数学操作。
    - LT, GT, SLT, SGT, EQ, ISZERO（对栈顶值是否为零判断）等比较操作返回 0 或 1（以 32 字节形式表示）。
- 位运算与字节提取：
    - AND/OR/XOR/NOT：按位操作，注意它们是位运算（bitwise），不是逻辑运算（logical）。例如两个非零字按 AND 后可能得零。
    - BYTE：从 32 字节词中取第 n 个字节（0..31）。
    - SHL/SHR/SAR：左移、逻辑右移、算术右移。
- 哈希与环境信息：
    - keccak256（有些实现称 SHA3）：用于计算内存片段的哈希，常用于 mapping 的键地址计算（storage slot = keccak256(concat(key, slot))）。
    - ADDRESS、BALANCE、ORIGIN、CALLER、CALLVALUE、CODESIZE、CODECOPY 等用于访问当前执行环境或外部合约信息。
    - BLOCKHASH, COINBASE, TIMESTAMP, NUMBER, DIFFICULTY 等用于区块相关的环境值（注意它们可作为“较弱的随机数”来源，但不可安全地作为高强度随机性来源）。
- 内存/存储指令：
    - MLOAD/MSTORE/MSTORE8/MSIZE：内存的读写操作（MSTORE 写 32 字节；MSTORE8 写 1 字节）。
    - SLOAD/SSTORE：读取和写入合约存储（storage），SSTORE 是昂贵的操作（gas）。
- 控制流：
    - JUMP/JUMPI：非条件与条件跳转。JUMP 要求跳转位置是一个以 JUMPDEST 标注的合法位置（避免跳到任意位置）；JUMPI 根据栈顶条件决定是否跳转。
    - PC、JUMPDEST、JUMPTABLE（间接形式的实现/编译时策略等）：合约的函数分发与 if/else/循环都通过这些跳转实现。
- PUSH/DUP/SWAP：
    - PUSH1..PUSH32：把立即数压栈（1..32 字节）。
    - DUP1..DUP16：复制栈顶第 N 个值到栈顶（可以直接访问前 16 个元素）。
    - SWAP1..SWAP16：与栈中第 N 个元素交换位置（限制同样是最多 16）。
- 日志/事件：
    - LOG0..LOG4：把记忆片段作为日志发布到交易的 logs 区域（事件/Topics 概念），可带 0 到 4 个 topics。事件检索通常通过 topics 索引（例如 transfer 的 topic0 通常是 keccak256("Transfer(address,address,uint256)")）。
    - 日志存储在链的日志/receipt/状态树（Merkle tree 的一部分供验证）中，可被轻节点或外部索引服务快速检索。
- 合约创建与外部调用：
    - CREATE/CREATE2：部署新合约。CREATE2 增加了 salt 输入，使得在给定发送者/salt/code 时地址可预计算（因此可以“挖出”具有特定前缀的地址，称为 vanity address）。
    - CALL/CALLCODE/DELEGATECALL/STATICCALL：消息调用的不同变体。CALL 是普通调用并可改变上下文为被调用者；DELEGATECALL 在调用时保持原调用者（msg.sender）与原合约的存储上下文（因此用于代理模式）；STATICCALL 只读调用，不能修改状态；CALLCODE（历史上存在）类似于 DELEGATECALL，但语义细微差异，已少用。
    - 每种调用会在栈上返回一个布尔值（是否成功），并且可以通过 RETURNDATASIZE / RETURNDATACOPY 获取外部调用返回的数据。
- 实战意义与开发注意：
    - 大多数合约逻辑由编译器将高级语句（如 if/else、for/while、函数调用）编译成上述 opcodes 的组合。分析字节码时，主要关注 dispatch（函数选择子匹配与 JUMPI 到具体函数体）与具体函数实现的 storage/memory 操作。
    - 某些“省 gas”或“隐藏意图”的技巧会使用非典型 opcodes 或动态 jump（通过 calldata 指定跳转位置），这会使反编译与符号执行复杂化。大多数 Solidity 编译器不会生成动态跳转，除非人为写 raw assembly。
    - 操作码的命名在不同资源上可能有别名（如 keccak256 有时被称为 SHA3 或 SHA_3），所以对照官方/权威资源（evm.codes、以太坊黄皮书、evm 实现等）非常重要。

## 3.3 控制流图（CFG）与函数分发（dispatcher）——分析字节码与反编译的关键

- 控制流图（Control Flow Graph, CFG）的本质：CFG 是字节码或反汇编后指令序列的抽象图，节点通常表示基本块（连续的一段指令、且仅在末尾可能有跳转），边表示可能的控制流（顺序执行、JUMP 或 JUMPI 的跳转）。通过构建 CFG，可以把线性的 opcode 列表组织成更容易理解的“函数体”、“分支”、“循环”等高层结构，有利于逆向工程与自动化反编译。
- 函数分发（dispatcher）模式：大多数由 Solidity 编译的合约在代码起始处会构造一个典型的“dispatcher”序列：
    - 先读取 calldata 的大小（CALLDATASIZE）与前 4 字节（用于 selector）。如果 calldata 长度不足（< 4），通常跳转到 fallback 或 receive 函数的实现。
    - 通过位操作（比如将 calldata 的前 32 字节加载到栈，右移、mask 等）提取前 4 字节的 selector（函数选择子）。
    - 将 selector 与一系列常量（函数签名的 selector 散列的前 4 字节）用 EQ / JUMPI 比较，并在匹配时 JUMP 到相应函数实现块。换言之：一连串的 “dup, push selector, eq, push target, jumpi” 构成 dispatcher。
    - 如果没有匹配到任何 selector，则执行 fallback/receive 的代码或 revert。
- 如何从字节码中识别函数体与 selector：
    - 在反汇编中观察 “匿名的比较链” 的模式（重复读取 calldata，mask、eq、jumpi），可以识别出哪些常量为 selector（例如 0x2e1a7d4d 在视频中就是某个函数的 selector）。
    - 工具（如 Heimdall）通过跟踪 JUMPDEST 的目标与 selector 常量的关系自动构建出函数列表，并且把每个函数体的基本块抽取出来，再结合 calldata 解码（基于已知 selector 与签名库的映射）来构建 ABI。
    - 使用控制流图可以更直观地查看合约如何在不同 selector 之间分派、不同分支如何处理 calldata、以及外部调用（CALL、DELEGATECALL）如何嵌入在执行路径中。
- 示例（Wrapped Ether 的简化流程）：
    - 视频示例里，WETH 合约的开头会 PUSH 一些值作为 free memory pointer（为 Solidity 在内存中保留位置），随后检查 CALLDATASIZE 是否小于 4（若是则进入 fallback），否则读取前 32 字节并施以除法与 AND mask 来获得前 4 字节的 selector。
    - 接着把 selector 与多个常数比较（例如 name()、transfer()、withdraw() 等），匹配之后 JUMP 到对应 block，执行函数体（如读 storage、更新 storage、发出事件或进行外部转账）。
- 反编译与工具链：
    - Heimdall、Ethersplay、evm-decompiler 等工具会把 CFG 可视化（树状或图形显示），并尝试把逻辑还原成 Solidity 样式的代码（包括变量名、ABI、事件名等），这在处理未验证（unverified）合约时尤其有用。
    - 要注意：反编译并非完美，编译器优化、内联 assembly、动态 jump、混淆等会使推断产生不确定性。工具通常会用 heuristic（启发式规则）和签名数据库（如 Etherface / 4byte.directory）来提高准确率。

## 3.4 Solidity 类型在 EVM 中的表示：地址、数值、mapping、动态类型与 RLP

- 基本思想：Solidity 的高层类型在编译后会映射为若干 EVM 原语的组合（32 字节槽、memory 编码、keccak256 地址算子等）。理解这些映射对于逆向、审计与 gas 优化都很关键。
- 固定宽度类型（uint、int、address、bytesN）：
    - 这些类型本质上都占一个或多个 32 字节的“词”（word）。uint256/ int256/ address（在 EVM 内部为 20 字节，但在算术处理时会被表示为 32 字节并且高位为 0）通常通过位掩码（AND）来截取有效位。视频举了“用 20 个 0xFF 字节掩码去获取 address”的例子：编译器常常对来自 calldata 或其他位置的字做 AND 掩码把高位清零，以确保变量被正确地当成地址处理。
    - 如果看到对一个 word 做乘、除、加、减等算术操作，通常可以推断这两个值是数值类型（uint/int），而不是字节序列（bytes）或文本。
- 字节/位类型（bytes、bytesN、byte 提取、位移）：
    - 当代码使用 BYTE、SHL/SHR、AND/XOR 等操作，通常说明在处理按字节或按位的内容（如从某个 word 中抽取特定位）。比如从 calldata 的某个 offset 提取字节，或从 storage 的某个 packed slot 中取出子字段。
- 动态类型（string、bytes、数组、struct）：
    - 动态类型无法在单个 32 字节内完全存储，因此通常放在内存并由 storage 中的 slot 存放其“指针/offset”或实际内容的起始位置。
    - 在 Solidity 的 storage 布局中，动态长度内容（如 bytes、string、动态数组）通常被放置到一个由 keccak256(slot) 确定的起始位置，storage 的主 slot 处保存长度或偏移信息，而实际内容则按照包（word）对齐写入连续的 storage slot（或保存在链下/使用其他合约来存储）。
- mapping（映射）的实现细节：
    - Solidity 的 mapping(keyType => valueType) 并不在一个连续空间按 key 索引；相反，它使用 keccak256(hash(abi.encodePacked(key, slot))) 的方式来计算存储位置（slot）。这里的 slot 是该 mapping 在合约 storage 中的固定槽编号（取决于编译器分配），而 key 在编码后与 slot 连接然后被哈希，产生的 32 字节哈希值作为实际存储位置。
    - 例如 mapping(uint256 => uint256) balances 在 storage slot 42，那么 balances[1] 实际存储在 keccak256(abi.encodePacked(uint256(1), uint256(42))) 的位置。这样设计避免了不同 mapping 之间的槽冲突（因为 slot 不同会改变哈希的最后部分），同时利用哈希的碰撞概率极低来保证隔离性。
    - 这种布局意味着无法按遍历所有 keys；需要外部索引或事件来检索 mapping 中的所有键/值。
- RLP 与 ABI 编码（视频中简述 rlp，但混合了两种概念，需要注意）：
    - 视频中提到 RLP（Recursive Length Prefix）编码，这是以太坊在底层（如节点间消息、某些交易序列化）中广泛使用的编码方式，用于序列化列表和字节串（主要用于以太坊协议级别的数据结构，而不是 Solidity 函数调用的 ABI 编码）。RLP 的基本思想是：在数据前面加上长度前缀，从而能够解析任意嵌套的列表结构。
    - Solidity 的 ABI 编码（用于函数调用和返回值）是一套不同但相似的规则：固定长度类型占 32 字节，动态类型在参数区存指针（offset），真正数据在尾部按 32 字节对齐并以长度前缀开头。虽然视频把 RLP 提到 EVM 中作为“通用序列化手段”，但更实际的是：ABI 与 RLP 都是“长度前缀”的思想，但在不同层面被使用（ABI 用于 contract 调用/返回，RLP 用于节点/链上数据结构）。
- 通过操作码特征判断类型的启发式方法（谨慎使用）：
    - 在逆向时，一些经验法则能帮助判断类型：若某值被 AND 掩码为 20 字节的 0xff..ff，通常表示这是 address；若对值进行算术 add/mul/div 操作，表明是数值；若使用 BYTE 或类似逐字节的操作，表明与 byte/bytesN/字符串相关；若见到 keccak256(concat(key, slot)) 并随后进行 SSTORE/SLOAD，通常表示 mapping 的存取。
    - 这些判断并非绝对规则，可能因编译器优化或手写 assembly 而偏离，因此在关键审计场景需结合更多上下文与测试。
- 小结：理解类型在 EVM 内的表示能极大提升对合约字节码的洞察能力：你可以通过 opcodes 模式、mask/shift/byte 操作以及 keccak256 的使用来判断变量的类型与存储形式，从而准确还原 ABI 或原因推断合约逻辑。

# 4. 框架 & 心智模型（Framework & Mindset）

下面抽象出从视频中可提炼的几套实战性 framework 与 mindset，帮助你系统化地分析与理解任意 EVM 合约，每一条至少展开 500 字详细说明。

Framework A — “由外到内”的反汇编与分析流程（步骤化方法）

- 核心思想：在分析未知合约或字节码时，先从外部可见信息入手（交易、calldata、logs、events），再逐步深入到字节码的控制流与存储布局。这个流程的优势在于可以快速获取有用的高层信息（函数签名、事件、是否有 fallback、是否存在 delegatecall/create2 等）并在此基础上有针对性地深入技术细节。
- 步骤详解：
    1. 收集外部数据：抓取与目标合约相关的链上交易、logs（事件 topics）、创建交易（若存在 create/create2）、交易 input（calldata）和 output（return data）。这一步可以借助 etherscan、Arbiscan 或自建节点的 RPC 来做。
    2. 从 calldata 提取 selector：对每个交互的 calldata 取前 4 字节，使用签名数据库（如 Etherface / 4byte.directory / 4byte.link）做查找。若匹配成功，可以获得可能的函数签名（注意可能有多重匹配）。把这些函数选择子与交易 hash 关联起来。
    3. 观察 logs 和 topics：解析 logs 的 topic0（通常是 keccak256("EventName(...)")），借助签名数据库可逆向出事件名称与 indexed 参数数量。日志常常帮助我们获取 mapping 操作（如 Transfer 事件对应 ERC-20 的余额变动），或者合约内部状态变更的线索。
    4. 反汇编字节码并构建 CFG：把合约字节码反汇编成 opcodes，并使用工具（Heimdall、evm.codes playground、IDA-like 工具）生成控制流图。识别 dispatcher 模式（selector 的一系列 eq+jumpi）并将之作为函数入口点的映射表。
    5. 针对感兴趣的函数生成符号执行或模拟执行：对潜在的危险函数（transfer、withdraw、delegatecall、selfdestruct、create2）进行符号执行或带样本数据的逐条 step-through（可以借助 Heimdall 的 VM/playground 功能），观察 stack/memory/storage 的变化与外部调用行为。
    6. 恢复高层表示（ABI/伪 Solidity）：使用反编译工具把底层操作块映射回可读的伪代码或生成 ABI。对关键的 storage slot 或 mapping 做哈希计算来定位 storage 地址（如 balances[addr] 的 slot）。
    7. 验证与测试：对推断出的函数签名与 ABI 进行调用（在本地测试链或 fork 的主网环境），使用 fuzzing 或符号输入来验证是否与反编译结果一致，并确认任何可能的漏洞路径（重入、未检查的外部返回值、权限检查缺失等）。
- 心得与注意事项：
    - 逆向是增量式的：先解决那些能用最少信息断定的部分（如事件名、是否有 fallback）、再去解更复杂的 mapping 布局或动态编码。
    - 工具并非万能：Heimdall、evm.codes 等大幅提高效率，但面对手写 assembly、混淆或动态 jump 时仍需人工干预与逻辑推断。
    - 数据驱动而非猜测：利用链上实际交易与日志作为证据来支持推断，避免仅凭字节码模式做断言。

Framework B — “安全第一”审计心智：关注外部调用、权限、持久化与随机性

- 核心思想：审计 EVM 合约时，优先检查那些跨账户/跨合约的危害操作，并把注意力按风险分层（高风险：外部调用与资金移动；中风险：权限管理与逻辑缺陷；低风险：gas 优化与可读性）。
- 要点与步骤：
    1. 外部调用检查（CALL/DELEGATECALL/CALLCODE/STATICCALL）：
        - 每次外部调用都可能带来重入（reentrancy）或未检查的返回值风险。特别是 DELEGATECALL 会在调用者的存储上下文执行被调用者的代码，若调用逻辑可被外部控制则可能造成存储污染或权限劫持。
        - 审计应定位所有外部调用点，检查前置条件（是否进行状态更改后再调用外部？是否存在 checks-effects-interactions 模式？）以及外部调用成功与否是否被正确判断（return value 的使用）。
    2. 权限与访问控制：
        - 检查所有写 storage 的分支是否被 access control（owner/modifier/role）保护。典型问题包括缺失 onlyOwner、初始化函数未保护导致代理合约可被重置等。
        - 对 create/CREATE2 等会生成新合约或代理的行为，检查是否可能被利用生成恶意合约地址或操控初始化参数。
    3. 资金安全（转账、回滚、紧急停止）：
        - 检查所有转账路径（call.value / transfer / send / low-level call）是否有边界检查、是否对失败做恰当处理（例如回滚或记录），是否允许任意地址接收 funds（如 selfdestruct 的目标地址）。
        - 考虑是否提供 pause/stop 功能（pause pattern），以及是否能被滥用。
    4. 随机性与外部数据：
        - 使用 block.timestamp、blockhash、block.number、coinbase 等作为随机数源通常是不安全的，审计时需提示这一点并建议使用链下或预言机（Oracle）等更强的随机性/外部数据源。
    5. 事件与可追溯性：
        - 确保合约在关键操作（如转移、授权、关键参数更改）中发出事件，便于链上监控与取证。考虑 gas 优化时不要牺牲必要的 logs。
- 实践建议：
    - 用最小权限原则（principle of least privilege）设计合约，减少管理员功能或对管理员操作进行时间锁、多签等保护。
    - 在调用外部（尤其不受信任的合约）前尽量完成状态更改（Checks-Effects-Interactions 模式）并在必要时使用 ReentrancyGuard 或互斥锁。
    - 用测试链与模糊测试（fuzzing）模拟多种交互序列以验证边界条件与异常路径。

Framework C — “代码可追溯化”与事件/日志设计心智

- 核心思想：因为链上无法轻易遍历 storage 的所有 keys，事件（logs）是对链上状态变化做外部索引与追踪的主要方式。合理设计事件不仅便于前端与索引服务使用，也能在合约不可变的情况下作为链上证据与审计轨迹。
- 详细阐述：
    1. 事件（LOG）与 topics：
        - LOG0..LOG4 对应事件带 0..4 个 topics（indexed 参数）。第一个 topic（topic0）通常为事件名的 keccak256 哈希（例如 keccak256("Transfer(address,address,uint256)")），其余 indexed 参数作为 topics 存储（每个 topic 32 字节）。
        - 使用 indexed 字段可以极大提高通过 topics 的链上搜索速度（如扫描某个地址的所有 Transfer 事件），但 indexed 的参数会额外收费 gas。
    2. 事件替代 storage：在某些场景下为了节省 gas，开发者会选择不将数据写入 storage，而是将信息写入 log（事件）。事件一旦写入并不会改变合约 storage，但链下索引服务（如 TheGraph）可以把事件解析为数据库记录，达到“仅需可检索但不必直接在合约 storage 中读取”的目的。
        - 风险：事件并不直接影响合约执行逻辑，并且事件并非“状态”，仅作为链外索引。因此把关键状态仅存在事件中不是安全替代（不能用于后续合约逻辑），但可用于降低链上存储成本并在链下构建索引层。
    3. 事件设计实践：
        - 保证关键操作（转账、授权、配置更改、紧急开关）都有对应事件，并且包含足够信息（addresses、amounts、reason、tx hash 等）。
        - 对于可能引发争议的操作（如管理员操作、回收、清算），事件应记录操作者与相关参数以保证可追溯性。
        - 仅把必要字段设为 indexed（每个事件最多 4 个 topics），以避免过高 gas 成本。
- 小结：事件/日志是链上可检索的主要手段，合理设计能降低审计与运维成本，同时提供强有力的链上证据。要明确事件与 storage 的不同语义与约束，避免把它们混淆为“存储替代方案”。

# 总结

这段视频提供了一个面向实践的 EVM 内部视角，从栈、内存、存储、calldata 的作用到字节码/操作码的细节，再到如何用控制流图理解合约的函数分发与执行路径，最后给出了反编译与审计的工具与方法（Heimdall、evm.codes、etherface、Foundry 等）。关键收获包括理解 EVM 的 256 位字模型、前 4 字节 selector 的重要性、操作码如何组合成高级语言结构、mapping 的 keccak256 地址计算、以及用 CFG + selector 匹配来构建 ABI/反编译合约的标准流程。实践上，建议采用“由外到内”的分析流程、关注外部调用与权限边界、并合理设计事件以便链上可追溯与离线索引。若需把某个具体合约（未验证字节码）一步步反编译为 ABI/伪 Solidity，我可以接着用 Heimdall 的输出或你提供的字节码做示范。