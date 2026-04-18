---
notion-id: 27778d23-e296-81fc-822f-d0f3b53d7e42
cover: "[[imgs/C++异步编程：用C++20协程重写Asio代理.jpeg]]"
Date: 2025-09-23
Last edited time: 2025-09-23T11:58:00
Tags: []
Link: https://youtu.be/icgnqFM-aY4?si=OoUPDWZ9WSlgwrRI
pic: https://img.youtube.com/vi/icgnqFM-aY4/hqdefault.jpg
Verification: unverified
Owner:
  - AI generation
---
# 1. Metadata

- Title: C++ 异步编程回顾与用 C++20 协程重写 Asio 异步代理（Talking Async 第一集）
- Author: Chris Kolhoff & Clemens（转写整理）

# 2. Overview

本视频以一个“中间人代理（man-in-the-middle proxy）”示例为线索，回顾了过去十年 C++ 与 Asio 在网络编程上的演进，从 C++11 风格的回调（callbacks）写法，讲到 Asio 引入的 completion token（完成令牌）机制、与 future、Boost.Coroutine/Boost.Fiber 的整合，再到 C++20 协程（coroutines）与 Asio 的 use_awaitable（可等待令牌）结合。演示了如何逐步把回调代码改为协程风格、引入无异常（no-throw）适配器、增加超时（watchdog / per-operation timeout）逻辑，并说明了 Asio 的新特性：每操作（per-operation）取消与组合 awaitable 的逻辑运算（logical or / logical and）如何支持更细粒度的取消控制和更简洁的并发结构。

# 3. 按照主题来梳理

## 3.1 示例程序与 C++11 回调实现（man-in-the-middle proxy 的基本流程与回调链）

- 示例目标与总体结构：视频开始以一个非常简单的代理程序为例（man-in-the-middle proxy）。程序监听本地端口（accept），每当有客户端连接时，向目标远端服务器发起连接（connect），连接建立后在两个方向上各自以异步读写链（read/write loop）转发字节：客户端→服务器 与 服务器→客户端。关键点是，每个已建立的连接都会产生两条并行的异步操作链，分别负责双向传输。主流程是：async_accept → async_connect → 启动 client→server 与 server→client 两个异步循环。
- C++11 回调实现细节：在 C++11 风格中，Asio 的异步接口典型形式是 foo(args..., completion_handler)。completion_handler 是一个可调用对象（例如 lambda），签名由异步操作的 completion signature 决定（比如 error_code、bytes_transferred 等）。函数本身返回 void（表示异步启动已完成，结果通过回调返回）。示例的 main 创建 io_context 和 acceptor，然后调用 listen（启动 async_accept），accept 的回调里创建一个 per-connection 对象（proxy），该对象持有客户端 socket，初始化一个服务器 socket 并调用 async_connect。当 connect 完成回调成功后，proxy 启动两条链：读客户端->写服务器 与 读服务器->写客户端，每次读完成的回调会触发写操作并在写完成后再次发起读，从而形成循环。代码中大量使用 lambda 回调，且每个异步操作都以回调回收处理结果并推进下一步。此实现的特征是“回调地狱（callback-heavy）”：控制流分散在多个回调中，逻辑以函数对象/绑定/捕获的方式传播状态，生命周期通常靠 shared_ptr 管理连接状态（因为多条并发链共享状态且可能延续至回调之外）。
- 线程与异步的说明：示例通常在单线程下运行（只靠 io_context 驱动事件循环），并非通过为每个操作创建线程；异步由操作系统提供 IO 就绪事件驱动，Asio 的 io_context 循环（run）接收就绪通知并调用 completion handler，从而实现非阻塞并发。视频强调这点以纠正误解：异步并不等同于多线程，很多异步服务器可以在单线程内高效运行。

## 3.2 Completion Token（完成令牌）与 async_result 的抽象：future、yield_context、use_awaitable

- 引入 completion token 的动机：在 C++11 时代 Asio 的接口最后一个参数是直接的 completion handler（回调），且异步函数返回 void。但在 2014-2015 年，引入了 completion token 的概念以增强调用方对异步结果传递形式的控制。函数签名改为 foo(args..., CompletionToken)，而返回类型不再固定为 void，而是根据传入的 CompletionToken 经由一个自定义点 async_result 推导出的类型。
- async_result 的角色与自定义点：async_result 是一个 traits / customization point，它接受三个输入：异步操作的 completion signature（即操作完成时会传出的参数类型）、异步实现本身、以及用户提供的 completion token。它将这三者组合并决定函数实际接受的 token 类型与函数返回的结果类型。例如如果 token 是一个普通的回调（completion handler），async_result 的默认行为是让函数返回 void，保留回调机制；如果 token 是 use_future，则 async_result 会把函数改造成返回 std::future，于是调用者可以以 future.get() 或 wait() 的方式等待结果。
- 常见的内置或第三方 completion token：
    - use_future：把回调风格转换为返回 std::future。错误用异常传播（如果操作以 error_code 表示失败，future 会以异常结束）。
    - yield_context（与 Boost.Coroutine 协作）：yield_context 允许使用“栈式协程（stackful coroutines）”，使异步调用看起来像同步代码——调用 async_xxx(yield[...]) 会在调用处挂起，直到操作完成后恢复，并直接返回结果（例如 size_t）。这需要 Boost.Coroutine 的支持。
    - Boost.Fiber token：类似作用但属于 Boost.Fiber 库，除了栈式协程外还提供 fiber 间同步工具。
    - use_awaitable（视频重点）：针对 C++20 的栈less 协程（stackless coroutines），use_awaitable 使得 async 函数在协程中可 co_await，并直接返回操作结果（如 size_t）。这让异步代码在语义和写法上更接近同步风格，但仍是非阻塞的。
- token 的适配与行为差异：不同 token 不仅改变调用者如何接收结果（callback、future、co_await、yield），还会影响错误传递（例如 future 会将 error_code 转为异常，use_awaitable 在默认行为下可能也有异常语义，或可通过适配器改变）。async_result 的可定制性还允许第三方库提供自己的 token，以集成其原有的并发模型（例如 Boost.Fiber）。

## 3.3 将回调链改写为 C++20 协程（co_spawn / use_awaitable 的逐步重构）

- 协程改写的总体思路：把原来用 lambda 回调表示的异步链逐步替换为返回 awaitable 的函数（返回类型从 void 变成 asio::awaitable 或 use_awaitable 推导出的类型）。核心改动包括：把 listen、proxy、transfer 等函数改为 awaitable（可 co_await），使用 co_spawn 在 io_context（或某个 executor）上启动顶层 awaitable，并用 co_await 在协程内等待子操作的结果。这样原本的回调递归/回环用循环与 co_await 表示，代码更像同步顺序逻辑，便于阅读与维护。
- 具体步骤与要点：
    1. 准备：引入 use_awaitable 的 using 或 using executor 的别名，方便代码中不重复写命名空间。
    2. 修改 listen：listen 从启动 async_accept 的回调链改为返回 awaitable（“awaitable void”），在循环中使用 co_await accept(socket, use_awaitable) 来阻塞协程直到 accept 完成；接收到的 socket 直接作为本地变量继续处理。由于 awaitable 是惰性的，构造它本身不会执行，必须用 co_spawn 或 co_await 将其激活；于是 main 里要用 co_spawn(ctx.get_executor(), listen(...), detached) 来真正启动监听器。
    3. 引入 proxy 函数：把 per-connection 逻辑抽成一个 awaitable proxy（参数传入已 accept 的 client socket 与 target endpoint）。proxy 内部需要并行运行两个方向的传输（client->server 与 server->client）以及可能的看门狗（watchdog）。并行启动通常通过 co_spawn（为其中一条链获取并指定 executor 并将其 detached），或通过组合 awaitable（见后面逻辑运算）。
    4. 编写 transfer（传输）协程：transfer 从某个 socket 读数据（co_await async_read_some/async_read），再 co_await 写入对端。使用循环（for/while）来代替 callback 递归，配合 try/catch 处理异常或错误。原来 shared_ptr 管理的共享状态可以在协程局部变量与 co_spawn 的作用域中改进生命周期管理（后面会进一步优化以消除 shared state）。
    5. 启动与生命周期：通过 co_spawn 指定 executor（例如从 socket 的 get_executor() 获得），并以 detached 或显式等待的方式决定是否忽略子协程返回值。注意：若使用 detached 而子协程抛异常，异常会被丢弃，需谨慎。
- co_spawn、detached 与 executor：co_spawn(executor, awaitable, completion_token) 用于在指定 executor 上启动一个 awaitable。detached 是常用的 completion token，表示不关心协程结果（类似 fire-and-forget）。executor 决定协程在何处运行：acceptor 生成的 socket 默认继承 acceptor 的 executor，这样在多数示例中是一致的（单线程 io_context），但也能在多线程/多 executor 场景中更加灵活地把任务调度到指定执行上下文。

## 3.4 错误处理与 no-throw 适配（tuple adapter）— 避免异常传播的方案

- 问题动机：默认的 use_awaitable/awaitable 在遇到以 error_code 表示的失败时，常常会把错误转换为异常抛出（即在 co_await 处以异常形式传播）。有些代码更喜欢显式检查 error_code 而不是异常。completion token 机制允许我们用适配器改变这一行为。
- tuple 适配器（as_tuple / no-throw awaitable）的使用：视频展示了如何通过把原本的 use_awaitable 再外包一层适配器（as_tuple）来构造一个新的 completion token（例：use_no_throw_awaitable = as_tuple(use_awaitable)）。该适配器会把原来的多参数完成签名（error_code, size_t）合并为单一的 tuple（error_code, size_t），从而避免默认的“第一个参数为 error_code 则抛异常”的行为。协程 co_await 此 awaitable 时会返回一个 tuple，调用者可以用结构化绑定（structured bindings）把 error_code 与 size_t 解构出来并做显式判断处理。
- 改写后的代码变化：
    - 每处原本返回 size_t 的 co_await async_read 应改为接收 std::tuple<error_code, size_t>，例如 auto [ec, n] = co_await async_read(..., use_no_throw_awaitable)。
    - 不再需要 try/catch 来捕获异步操作抛出的异常，错误由 ec 显式检查并据此退出循环或进行资源关闭（close sockets）。
    - 连接 accept 的结果也变为 tuple（error_code + socket），accept 返回的 socket 仍需解构后使用。
- 优点与权衡：这种方式使错误传播更显式、可控，减少异常控制流对代码可读性的影响。但必须在代码中显式判断并处理 error_code（比异常驱动更冗长但更确定）。同时，适配器是通过 async_result 的可定制点实现，不改变底层异步实现，只改变调用/返回约定。

## 3.5 超时策略：watchdog（deadline）与 per-operation timeout（基于 timer 的组合）

- 两种超时策略定位与差异：
    1. Watchdog（基于 deadline）：为每个连接维护一个 deadline（steady_clock::time_point），在每次成功读写循环时把 deadline 往后延长（例如延后 5 秒）。同时启动一个独立的协程（watchdog），它用一个单独的定时器周期性检查当前时间是否超过 deadline；若超过则执行“关闭连接”的操作（close sockets）。这种方式的优点是节省定时器资源：只有一个 watchdog 定时器在运行并周期性唤醒来检查，而不是每次读写都新建定时器。缺点是粗粒度：watchdog 可能会在一侧关闭导致另一侧仍有数据待写丢失。
    2. Per-operation timeout（基于每次操作的 timer，与 logical or 组合）：不使用共享 deadline，而是将每次读或写与一个 timeout awaitable 组合成“logical or”。逻辑上，读操作与一个 timer 的 co_await 用 or 组合：co_await (async_read(...) || timeout(duration)). 组合的结果是一个 variant：如果 timeout 先完成则 variant 指示超时并可以立即返回/退出，否则取出读操作的结果并继续写。这样超时粒度更细：每个具体操作都有超时约束，能更精确地取消长时间阻塞的单次 IO，而不会强行关闭整条连接（除非业务需要）。
- watchdog 具体实现要点：
    - 在 shared state（或后来的局部结构）中保存 deadline 时间点。
    - watchdog 协程循环：co_await timer.expires_at(next_deadline) 或以小周期 sleep 检查；当 now >= deadline，关闭 sockets（或发出取消信号）。
    - 需要确保 watchdog 与 transfer 之间的取消/关闭语义：直接 close 会取消所有 socket 上的异步操作（在旧 Asio 中），但当引入 per-operation cancellation 时，可能只想取消部分链。
- per-operation timeout 的实现要点与返回处理：
    - 使用一个辅助协程 timeout_after(duration) 返回一个 awaitable，它创建一个 steady_timer、expires_after(duration)、co_await timer.async_wait(use_awaitable)。
    - 对读写使用 logical or：auto v = co_await (async_read(...) || timeout_after(dur)); 返回一个 variant。检查 variant.index() 或用 std::get_if/holds_alternative 来判断是超时还是读写完成；超时则退出当前 transfer。
    - 对写也同理，可能写操作的超时值不同（例如写可以更短或更长）。
    - 该方案避免了 global watchdog 的粗暴断开带来的数据丢失问题，但会为每次操作产生 timer 对象与调度开销，若操作频繁会有显著性能开销。
- 性能考量：视频指出 watchdog 对高吞吐场景更高效，因为它减少了定时器创建/销毁的频度；而 per-operation timeout 的粒度更细，逻辑更直观但可能带来较多定时器开销。实务中应按场景权衡选择。

## 3.6 每操作取消（per-operation cancellation）与 awaitable 逻辑组合（logical or / logical and）

- 每操作取消的引入背景：在旧版本 Asio 中，关闭 socket 会导致该 socket 上所有挂起的异步操作被取消（粗粒度）。Asio 1.19+ 引入了 per-operation cancellation 槽（cancellation slot）机制，使得可以向特定的异步操作传递取消信号而非全局关闭，支持更细粒度的取消控制。
- cancellation slot 的工作方式（高层描述）：每个异步操作会关联一个 cancellation slot（可被复用）。该 slot 是一个用于传递取消请求的轻量化位掩码/信号机制。向 slot 发出取消请求后，槽下游的正在进行的异步操作（比如 async_read 或 async_wait）将接收到取消并尽可能地终止自己，然后把取消结果传回上层。从用户层面通常无需直接管理低层位掩码（bitmask），而是通过 Asio 的高层 awaitable 合成接口让取消自动传播。
- awaitable 的逻辑组合：
    - logical or (||)：把多个 awaitable 并行启动，结果是“任一完成即满足”的语义。实现上，它会在第一个完成的 awaitable 上短路并对其他 awaitable 发出取消信号，co_await 该 or 表达式会在所有参与 awaitable 完全完成后（包括被取消的那些）才返回，以确保资源和状态清理完成。or 的返回类型是 variant（因为只有一个分支会产生实际结果），并且会短路触发取消到未完成分支。
    - logical and (&&)：等待所有 awaitable 都完成，返回结果为 tuple（各分支结果的组合）。and 更适合需要等待多个并行任务全部完成的场景。
- 在示例中的运用：
    - 把 client->server transfer、server->client transfer、watchdog 放在一个 or 组合中：co_await ( client_transfer || server_transfer || watchdog )，使得如果任一先完成（比如 watchdog 超时），就会取消其他两个传输链并等待它们完成清理。这样实现了“任一完成即触发取消并统一清理”的语义。
    - 为了让两条传输在独立 deadline 下互不干扰，示例还演示了把每个传输与自己的 watchdog（或单独 timeout）组合成或，然后用 and 将它们组合起来，从而实现更细粒度的取消与等待策略。
- 组合返回类型与值合并：视频说明了 or 返回 variant，and 返回 tuple。若组合中各分支有不同返回类型，and 会将它们组合成 tuple，or 则组合成 variant（即“哪一分支完成就用 variant 表示是哪种结果”）。这也决定了调用代码如何解构和处理返回值。

# 4. 框架 & 心智模型（Framework & Mindset）

- 框架一：从“回调链”到“协程顺序式控制”的迁移步骤（可作为改写异步程序的通用流程）
    1. 理解现有回调结构：识别入点（accept）、建立点（connect），以及后续的并行链（双向 transfer）。标记每个链的边界与共享状态（例如 sockets、缓冲区、deadline）。
    2. 为每个逻辑单元提炼为独立函数（或对象方法）：把 accept、proxy（per-connection 的入口）、transfer（单向传输）、watchdog/timeout 各自定义为单独单元。单元之间通过明确参数传递（socket、deadline、executor）而非隐式共享 state，便于后续转换。
    3. 将这些函数改造成 awaitable（即返回 asio::awaitable 或通过 use_awaitable 推导的类型）。把原本在回调中推进流程的地方改为在协程中使用 co_await 获得结果或等待完成。把回调的嵌套逻辑替换为顺序循环（for/while），利用结构化绑定获取操作结果（如果使用 as_tuple/no-throw）。
    4. 用 co_spawn 在适当的 executor 上启动最顶层协程。注意 executor 的传递与获取（socket.get_executor() 可作为子协程的 executor），并决定是否使用 detached（忽略结果）或其它 completion token（处理结果/异常）。
    5. 用 awaitable 逻辑组合（or / and）表达并行与竞争场景：若需要“任一完成时取消其它并等待清理”，用 or；若需要“全部完成再继续”，用 and。
    6. 错误与取消语义：选定错误传播策略（异常 vs error_code），并在需要时使用 as_tuple 等适配器控制异常行为。为取消使用 per-operation 取消槽或通过 close 进行全局取消，视需求而定。最后进行清理与资源释放（让局部变量出作用域以触发 RAII）。
该框架的核心心智是“把异步控制流显式化并序列化（用协程），把并发点用组合表达”，从而把代码从“事件驱动的分散控制”重构为“顺序但非阻塞的逻辑”，更利于可读性与正确性。
- 心智模型二：异步抽象层次与自定义点（async_result / completion token）
    1. 把异步 API 看作“三个要素”的组合：操作的签名（completion signature）、操作的实现、以及调用者期望的完成语义（completion token）。async_result 是把这三者结合并产生最终 API 的“适配器”。
    2. 选择合适的 completion token 即是在选择“调用体验”：回调（callback）适合极致低层的最小开销；future 适合与现有 blocking 风格过渡；yield_context / Boost 库适合已在该协程模型下的代码基；use_awaitable 适合 C++20 协程的新风格。理解这一点意味着你可以用同一套底层实现为不同调用者提供不同同步/异步体验，而无需改动实现。
    3. 在实际设计中，把错误传递策略（异常 vs error_code）看作 API 设计的显式契约。使用 async_result 的适配器（如 as_tuple）可以改变这一契约，使库更灵活地适配使用者期望。
该心智模型帮助开发者在设计异步库或重构异步代码时，把“实现”与“使用体验”解耦，并利用 async_result 这一可定制点实现多样的用户 API。
- 心智模型三：取消与超时的两种语义——“关闭导致取消”与“基于信号的 per-operation 取消”
    1. 传统模式（关闭-导致取消）：通过关闭 socket 等资源来迫使挂起的操作失败，这种方式语义简单、实现直接，但粗暴，会影响同一连接上仍有未完成工作的其他链。适合简单场景或当关闭整条连接是预期行为时。
    2. 精细控制模式（per-operation 取消）：通过 cancellation slot 把取消信号精确地送到某个操作或某个链，使得其他并行链可以继续或进行不同的清理路径。配合 awaitable 逻辑组合（or / and），可以实现“某一分支先完成则取消其它分支并在所有分支清理完后继续”的复杂控制流。
    3. 超时实现权衡：若希望最小化 timer 开销且不介意粗粒度断开，用 watchdog；若要保证每个操作有独立时限，或不能因一侧超时丢弃另一侧未发送的数据，则用 per-operation timeout 与 or 组合。选择依据是性能预算 vs 语义精细程度。
这一心智模型帮助架构师在实现超时与取消逻辑时做出权衡：明确是否优先资源开销还是数据完整性与粒度控制。

# 总结

视频通过一个逐步重构的案例，从回调式 Asio 编程过渡到 C++20 协程风格，详尽展示了 completion token、async_result 的强大适配能力、use_awaitable 的协程集成、错误适配（as_tuple/no-throw）、超时策略（watchdog 与 per-operation timeout）以及 Asio 新增的 per-operation cancellation 与 awaitable 逻辑组合（or/and）。整体目标是演示如何把复杂的异步控制流整理为更直观、可组合且更易维护的协程化结构，同时保留灵活的错误与取消策略以满足不同场景的需求。源码与 Asio 1.19+ 的相关特性可见视频中给出的 GitHub 链接与 Asio 官方链接（视频原文提及）。