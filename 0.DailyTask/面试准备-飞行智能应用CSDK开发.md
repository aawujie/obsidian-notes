# 飞行智能应用 CSDK 开发 — 一面准备手册

> 面试时间：明天 19:00
> 岗位：飞行智能应用 CSDK 开发
> 策略：一面大概率是技术面，C++ 基本功 + 项目深挖 + 领域基础

---

## 一、自我介绍（30 秒，背熟）

> 面试官好，我叫xx，5 年 C++/Python 开发经验，一直做自动驾驶底层系统开发。
>
> 在禾多科技做了 3 年纯 C++ 开发，负责过激光雷达/IMU/GNSS 等传感器的驱动和集成、Autosar 域控算法到 x86 平台的迁移，对多传感器融合、时间同步、CAN 通信都比较熟。
>
> 目前在元戎启行负责 HIL 自动化测试平台，从架构设计到 CI/CD 到监控看板都是独立或主导做的，支撑 36 万条自动化用例、14 个业务域的调度。
>
> 我对这个方向特别感兴趣，因为自动驾驶和无人机在传感器、通信、实时系统这些底层技术上是高度相通的，我的经验可以直接迁移过来。

---

## 二、C++ 必考 20 题（一面大概率出，每题能口头讲 1 分钟）

### 内存管理

**Q1: new/delete 和 malloc/free 的区别？**

- new 是运算符、可重载，malloc 是函数
- new 自动算类型大小并调构造函数，malloc 要手动算字节数
- new 失败抛异常，malloc 返回 NULL
- 配对使用：new→delete，malloc→free

**Q2: 内存泄漏怎么排查？**

- 工具：valgrind --leak-check=full、AddressSanitizer
- 预防：优先用智能指针代替裸指针、RAII

**valgrind --leak-check=full 详解：**

```
valgrind --leak-check=full ./your_program
```

- `--leak-check` 控制检测力度：`summary` 只输出总量摘要，`full` 打印每一处泄漏的**完整调用栈**，精准定位哪行代码分配了内存却没释放
- 会区分四类泄漏：
  - **definitely lost**：确定泄漏——没有任何指针指向这块堆内存，最严重，必须修
  - **indirectly lost**：间接泄漏——主指针丢了，附属内存跟着漏
  - **possibly lost**：疑似泄漏——指针指向内存中间而非开头，可能是故意设计
  - **still reachable**：程序退出时仍有指针持有但没释放——不算 bug，系统自动回收，但最好显式释放
- 常搭配 `--show-leak-kinds=all` 显示所有类型泄漏的详情
- 运行速度会大幅变慢（valgrind 插桩模拟内存管理），**只用于调试，不用于生产环境**
- 同时还能检测：野指针读写、缓冲区溢出、重复 free、栈溢出等非法内存操作

**Q3: 智能指针怎么选？怎么用？**

```
unique_ptr — 独占所有权，不能拷贝只能移动，开销接近裸指针
shared_ptr — 共享所有权，引用计数（原子操作），有开销
weak_ptr   — 配合 shared_ptr 打破循环引用，不增加引用计数
```

- 默认用 unique_ptr、需要共享才用 shared_ptr

**shared_ptr 的控制块（Control Block）详解：**

**shared_ptr 内部有两个指针**：一个指向对象，一个指向**控制块**。**控制块里存着**：

```
┌─── 控制块 (Control Block) ───┐
│  shared_count  (引用计数)     │  ← 有几个 shared_ptr 指向对象
│  weak_count    (弱引用计数)   │  ← 有几个 weak_ptr 指向对象
│  deleter       (删除器)      │  ← 自定义析构逻辑
│  allocator     (分配器)      │  ← 自定义内存分配
└──────────────────────────────┘
```

- **引用计数用 `std::atomic` 操作**，所以多个线程同时拷贝/销毁 shared_ptr 是**线程安全**的
- 但**对象本身不受保护**——**多线程同时读写对象内容仍需加锁**
- **`make_shared<T>()` 一次性分配对象+控制块（内存连续，效率最高）**，**`shared_ptr<T>(new T)` 两次分配（不推荐）**
- **控制块创建时机：首次构造 shared_ptr 时创建**，之后拷贝 shared_ptr 时复用同一个控制块

**Q4: 怎么实现一个简易 shared_ptr？**

```cpp
template<typename T>
class SimpleSharedPtr {
    T* ptr_;
    int* ref_count_;
public:
    explicit SimpleSharedPtr(T* p) : ptr_(p), ref_count_(new int(1)) {}
    SimpleSharedPtr(const SimpleSharedPtr& other)
        : ptr_(other.ptr_), ref_count_(other.ref_count_) {
        ++(*ref_count_);
    }
    ~SimpleSharedPtr() {
        if (--(*ref_count_) == 0) {
            delete ptr_;
            delete ref_count_;
        }
    }
    T* operator->() { return ptr_; }
    T& operator*() { return *ptr_; }
};
```

### 面向对象

**Q5: 虚函数表怎么工作的？**

- 每个有虚函数的类有一张 vtable，存在**只读数据段**
- 每个对象有一个 vptr 指向所在类的 vtable
- 构造函数中逐级设置 vptr：先基类构造→基类 vptr，再派生类构造→派生类 vptr
- 所以构造函数中调虚函数不会多态

**Q6: 虚析构函数为什么需要？**

```cpp
Base* p = new Derived();
delete p;  // 如果 Base 析构函数不是 virtual，只调了 Base::~Base()
           // Derived 的资源没释放，内存泄漏
```

**Q7: 重载(overload) vs 重写(override)？**

- 重载：**同一作用域，函数名相同、参数不同**，编译期决议
- 重写：派生类覆盖基类虚函数，**签名完全一致，运行期多态**
- override 关键字**让编译器帮你检查是不是真的重写了**

### C++11+ 新特性

**Q8: move 和 forward 区别？**

- **std::move 只是类型转换，真正转移资源的是移动构造函数**

```cpp
// move: 无条件转右值
int&& x = std::move(a);  // a 变右值

// forward: 有条件转发（左值转左值，右值转右值）
template<typename T>
void wrapper(T&& arg) {
    foo(std::forward<T>(arg));  // 完美转发
}
```

**forward 的本质：模板推导 + 引用折叠**

`forward` 底层就是 `static_cast`，关键是模板参数 T 携带了"原始值是左值还是右值"的信息：

```cpp
// forward 简化实现
template<typename T>
T&& forward(remove_reference_t<T>& arg) noexcept {
    return static_cast<T&&>(arg);
}
```

| 调用 | T 推导为 | `T&&` 折叠后 | forward 返回 |
|---|---|---|---|
| `wrapper(a)` (a 是左值) | `int&` | `int& && → int&` | 左值 |
| `wrapper(10)` (10 是右值) | `int` | `int&&` | 右值 |

**一句话对比：** move 和 forward 底层都是 `static_cast`，区别在于 move 无条件转右值，forward 通过模板推导决定是否转右值。

**Q9: 左值和右值怎么区分？**

- 简单判断：**能取地址（&x）的是左值，不能的是右值**
- 左值：**有名字的变量、可以出现在赋值号左边**
- 右值：**字面量、临时对象、move 的结果**

**三类右值的存放位置（面试加分项）：**

| 右值类型                 | 存放位置          | 特点                     |
| -------------------- | ------------- | ---------------------- |
| 字面量（`42`、`"hello"`）  | 代码段 `.rodata` | 编译期确定，只读，程序运行全程存在      |
| 临时对象（`a+b`、函数返回的临时值） | 栈（或寄存器）       | 表达式结束后立即析构，编译器会 RVO 优化 |
| move 的结果             | 堆（接管原对象资源）    | move 本身不分配内存，只是指针转移    |

```cpp
// 字面量：存在 .rodata，不能写
int x = 42;                    // 42 是字面量，存在只读数据段
const char* s = "hello";       // "hello" 也存在只读数据段

// 临时对象：在栈上，表达式结束就析构
int y = a + b;                 // a+b 的结果是临时值，通常放寄存器
std::string s = getStr() + " world";  // getStr() 返回的临时对象在栈上

// move 的结果：不分配新内存，只是指针转移
std::string s1 = "hello";
std::string s2 = std::move(s1);  // s2 接管 s1 的堆内存，s1 被置空
// std::move 只是类型转换，真正转移资源的是移动构造函数
```

**注意：** **右值引用变量本身有名字，是左值！**

```cpp
int&& r = std::move(x);   // r 有名字 → r 是左值
int&& r2 = 42;            // r2 有名字 → r2 也是左值
```

**被 move 后的对象还能用吗？**

**不会报错，但内容是空的。** 被 move 的对象处于"有效但未指定"（valid but unspecified）状态：

```cpp
std::string s1 = "hello";
std::string s2 = std::move(s1);

std::cout << s1;        // 输出空字符串 ""，不会崩溃
std::cout << s1.size(); // 输出 0
s1 = "world";           // ✅ 可以重新赋值，继续正常使用
```

- 标准库类型（`string`、`vector`、`unique_ptr`）：move 后保证合法——**string/vector 变空，unique_ptr 变 nullptr**
- 自己写的类：移动构造函数里必须把原对象的指针置空（`other.ptr_ = nullptr`），否则析构时 double free
- 关键原则：move 后可以调用**没有前置条件**的方法（`.empty()`、赋值），但不能假设数据还在

**Q10: lambda [=] 和 [&] 的区别？**

- [x] 按值捕获，lambda 内只读，捕获的是当前值的一个拷贝
- [&] 按引用捕获，可以修改，但要注意生命周期——lambda 在外部变量销毁后执行会悬空
- 捕获 this 可以用 [this] 或 [=]（隐式）

**Q11: constexpr 和 const 的区别？**

- const：**运行期不可修改，但不一定编译期已知**
- constexpr：**强制编译期求值**，可以**用来定义数组大小、模板参数**
- C++14 起 constexpr 函数可以包含循环和分支

```cpp
// const：值可能编译期未知
const int a = 10;      // 编译期常量
const int b = rand();  // 运行期才确定，编译期不知道值

int arr1[a];   // ✅ 编译期常量，可以
int arr2[b];   // ❌ 编译期不知道值，不可以

// constexpr：强制编译期求值
constexpr int c = rand();  // ❌ 编译报错
constexpr int d = 10;      // ✅ 一定是编译期常量

// C++14 起 constexpr 函数可以很复杂
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}
int arr[factorial(5)];  // ✅ 编译期算出 120
```

**`constexpr` 函数不是"必须编译期执行"：**

`constexpr` 标记的是函数**有能力**在编译期求值，不是强制。能不能编译期算，取决于参数是不是编译期常量：

```cpp
// 参数是编译期常量 → 编译期算
constexpr int a = factorial(5);    // ✅ 编译期算出 120
int arr[factorial(5)];             // ✅ 编译期算出 120

// 参数是运行期变量 → 运行期算
int n;
std::cin >> n;
int b = factorial(n);              // ✅ 运行期计算，可以
// int arr2[factorial(n)];         // ❌ 编译期不知道 n，不行
```

**`constexpr` 变量 vs `constexpr` 函数——面试高频混淆点：**

|                    | 编译期求值        | 运行期求值        |
| ------------------ | ------------ | ------------ |
| `constexpr` **变量** | ✅ 必须，否则编译报错  | ❌ 不允许        |
| `constexpr` **函数** | ✅ 可以（参数是常量时） | ✅ 可以（参数是变量时） |

```cpp
constexpr int x = 10;           // ✅ 变量，必须编译期
constexpr int y = rand();       // ❌ 编译报错，rand() 编译期算不出来

constexpr int f(int n) { return n * 2; }
constexpr int a = f(10);        // ✅ 编译期算
int b = f(rand());              // ✅ 运行期算，没问题
```

**一句话总结：** const 是"运行期不能改"，constexpr 是"编译期就能算出来"。constexpr 的东西一定是 const 的，但 const 的东西不一定是 constexpr 的。

**`constexpr` 函数 vs `const` 成员函数——面试高频混淆点：**

```cpp
class Foo {
    int val_;
public:
    // const 成员函数：承诺不修改成员变量
    int getVal() const {        // ← const 修饰的是函数本身
        // val_ = 10;           // ❌ 编译报错
        return val_;
    }

    // constexpr 函数：返回值可以编译期算出来
    constexpr int doubleVal() const {  // 两个可以同时用
        return val_ * 2;
    }
};

void bar(const Foo& f) {
    f.getVal();    // ✅ const 对象只能调 const 成员函数
    f.setVal(10);  // ❌ 非 const 函数不能调
}
```

| | `const` 成员函数 | `constexpr` 函数 |
|---|---|---|
| 修饰什么 | 函数行为（承诺不改成员） | 返回值（可以编译期求值） |
| 能用于 | 只能成员函数 | 成员函数、普通函数都可以 |
| 关键作用 | const 对象只能调 const 函数 | 返回值可以当数组大小、模板参数 |
| 修饰返回值 | 语义不同，很少用 | — |

```cpp
// const 修饰返回值（很少用，只有返回引用/指针时才有意义）
const int  foo() { return 5; }       // 没意义，调用者拿的是拷贝
const std::string& getName() const;  // 有意义，防止调用者修改内部数据
```

### STL

**Q12: vector 扩容机制？**

- **gcc 是 2x 扩容，msvc 是 1.5x**
- 扩容过程：分配新内存 → 移动/拷贝元素 → 释放旧内存
- resize() 改变 size，**reserve() 只分配 capacity 不初始化**
- **扩容导致所有迭代器失效**

**Q13: map vs unordered_map？**

| | map | unordered_map |
|---|---|---|
| 底层 | 红黑树 | 哈希表 |
| 查找 | O(log n) | O(1) 平均 |
| 有序 | 是 | 否 |
| 内存 | 较小 | 较大（桶数组） |

**Q14: 迭代器什么时候失效？**

- vector：**扩容时全部失效；insert/erase 之后插入点之后的失效**
- map/unordered_map：**只有被 erase 的元素失效**，其他不受影响
- list：**只有被 erase 的元素失效**

### 多线程

**Q15: lock_guard 和 unique_lock 的区别？**

- lock_guard：**最简单的 RAII**，构造加锁析构解锁，不能手动解锁
- unique_lock：**更灵活，可以手动 unlock/lock、可以用 condition_variable、可以延迟加锁**

**Q16: 死锁怎么避免？**

- 四条件：**互斥、持有等待、不可剥夺、循环等待**
- 避免：**固定加锁顺序 + std::lock() 同时锁多个 + try_lock 超时放弃**

**Q17: 实现一个线程安全的单例？**

```cpp
class Singleton {
public:
    static Singleton& getInstance() {
        static Singleton instance;  // C++11 保证线程安全
        return instance;
    }
private:
    Singleton() = default;
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
};
```

**`static` 局部变量为什么线程安全？**

C++11 标准规定：函数内的局部 static 变量**初始化只执行一次**，多线程同时进入时，**编译器自动加锁保护**。原理：

- 编译器在背后生成一个**隐藏的 guard 变量**（一个标志位）
- 第一个线程进入时，检查 guard 标志 → 未初始化 → 执行构造 → 设 guard 为"已初始化"
- 其他线程同时进入时，检查 guard 标志 → 正在初始化中 → **阻塞等待**，直到第一个线程完成
- 之后再进入的线程，检查 guard 标志 → 已初始化 → 直接跳过，返回实例引用

等价于编译器帮你写了：

```cpp
static Singleton* instance = nullptr;
static std::once_flag flag;
static bool initialized = false;

if (!initialized) {
    std::call_once(flag, [] {
        instance = new Singleton();
        initialized = true;
    });
}
return *instance;
```

**一句话：** C++11 把"双检查锁"（DCLP）的坑由编译器帮你填了，用函数内 static 变量就是最简单、最安全、最高效的单例写法。

### 编译与底层

**Q18: 编译四个阶段？**

**预处理（宏展开、#include）→ 编译（源码→汇编）→ 汇编（汇编→.o）→ 链接（.o→可执行文件/库）**

**Q19: 静态库 vs 动态库？**

- 静态库 .a：编译时嵌入可执行文件，文件大但独立，更新需重新编译
- 动态库 .so：运行时加载，文件小可共享，**更新不需重新编译**，但 ABI 兼容是风险

**Q20: 什么是 ABI 兼容？**

- ABI（Application Binary Interface，应用程序二进制接口）兼容：**改了 .so 但 .h 接口不变**，老的可执行文件能直接跑，不需要重新编译
- **破环 ABI 兼容**：删虚函数、改类大小（加成员变量）、改函数签名——这些都会改变二进制层面的符号表和内存布局
- **保证 ABI 兼容**：**pimpl 模式（隐藏实现细节）**、**接口类只放纯虚函数**
- 与 API 的区别：API 是源码级兼容（**编译通过**），ABI 是二进制级兼容（**链接通过**）

---

## 三、手撕代码 6 题（写出来，不只是看懂）

### 1. 线程安全单例（必考）

```cpp
class Singleton {
public:
    static Singleton& getInstance() {
        static Singleton instance;
        return instance;
    }
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
private:
    Singleton() {}
};
```

### 2. 简易 shared_ptr（高频）

```cpp
template<typename T>
class SharedPtr {
    T* ptr_ = nullptr;
    int* ref_count_ = nullptr;
public:
    explicit SharedPtr(T* p = nullptr) : ptr_(p), ref_count_(new int(1)) {}
    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), ref_count_(other.ref_count_) {
        if (ref_count_) ++(*ref_count_);
    }
    SharedPtr& operator=(const SharedPtr& other) {
        if (this != &other) {
            release();
            ptr_ = other.ptr_;
            ref_count_ = other.ref_count_;
            if (ref_count_) ++(*ref_count_);
        }
        return *this;
    }
    ~SharedPtr() { release(); }
    T* operator->() { return ptr_; }
    T& operator*() { return *ptr_; }
    int use_count() const { return ref_count_ ? *ref_count_ : 0; }
private:
    void release() {
        if (ref_count_ && --(*ref_count_) == 0) {
            delete ptr_;
            delete ref_count_;
        }
    }
};
```

### 3. 环形缓冲区

```cpp
template<typename T>
class RingBuffer {
    std::vector<T> buf_;
    size_t head_ = 0, tail_ = 0, size_ = 0;
    const size_t capacity_;
public:
    RingBuffer(size_t cap) : buf_(cap), capacity_(cap) {}
    bool push(const T& item) {
        if (size_ == capacity_) return false;
        buf_[tail_] = item;
        tail_ = (tail_ + 1) % capacity_;
        ++size_;
        return true;
    }
    bool pop(T& item) {
        if (size_ == 0) return false;
        item = buf_[head_];
        head_ = (head_ + 1) % capacity_;
        --size_;
        return true;
    }
    bool full() const { return size_ == capacity_; }
    bool empty() const { return size_ == 0; }
};
```

### 4. 生产者-消费者（线程安全队列）

```cpp
template<typename T>
class BlockingQueue {
    std::queue<T> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;
    bool stopped_ = false;
public:
    void push(T item) {
        std::lock_guard<std::mutex> lock(mutex_);
        queue_.push(std::move(item));
        cv_.notify_one();
    }
    bool pop(T& item) {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this] { return !queue_.empty() || stopped_; });
        if (queue_.empty()) return false;
        item = std::move(queue_.front());
        queue_.pop();
        return true;
    }
    void stop() {
        std::lock_guard<std::mutex> lock(mutex_);
        stopped_ = true;
        cv_.notify_all();
    }
};
```

### 5. 反转链表

```cpp
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
        ListNode* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}
```

### 6. LRU Cache

```cpp
class LRUCache {
    int capacity_;
    std::list<std::pair<int, int>> cache_;  // 头部是最近使用的
    std::unordered_map<int, decltype(cache_)::iterator> map_;
public:
    LRUCache(int cap) : capacity_(cap) {}
    int get(int key) {
        auto it = map_.find(key);
        if (it == map_.end()) return -1;
        cache_.splice(cache_.begin(), cache_, it->second);
        return it->second->second;
    }
    void put(int key, int value) {
        auto it = map_.find(key);
        if (it != map_.end()) {
            it->second->second = value;
            cache_.splice(cache_.begin(), cache_, it->second);
            return;
        }
        if (cache_.size() >= capacity_) {
            map_.erase(cache_.back().first);
            cache_.pop_back();
        }
        cache_.emplace_front(key, value);
        map_[key] = cache_.begin();
    }
};
```

---

## 四、项目深挖话术（每个项目 3 分钟版本）

### 项目 1：IFC SIL 仿真平台（最重要，最接近 CSDK）

**一句话概括：** 把 Autosar 域控算法从嵌入式平台迁移到 x86，让开发者在 PC 上完成全部调试，不用实车和域控硬件。

**面试话术：**

> 这个项目的核心需求是让算法工程师在自己的 PC 上就能跑 IFC 域控的完整算法链路，摆脱对实车和域控硬件的依赖。我做了三件事：
>
> 第一，把 Autosar 通信栈和应用层模块从 ARM 平台迁移到 x86 Linux。Autosar 的 RTE 层高度依赖特定 OS 和硬件，我做了一层平台抽象，用条件编译区分 x86 和 ARM，上层的应用代码不用改。
>
> 第二，用 Unity 仿真引擎替代真实传感器。摄像头数据、车身信号由 Unity 模拟，CAN 控制信号由测试用例注入，实现了 PC 端完整的"感知→决策→控制"闭环。
>
> 第三，交付了完整的 x86 编译工具链和 SDK 软件包，包括 CMake 构建脚本、运行时库、使用文档，新来的开发人员半天就能搭建环境。
>
> 这个项目本质上是一次 SDK 开发——把硬件依赖抽象掉，为上层提供统一的平台无关接口。这和 CSDK 设计思路完全一致。

**可能的追问：**

- "怎么保证仿真和实车一致性？" → 通信接口一致（同一套 CAN 协议定义）、传感器数据时间戳模拟真实传感器频率、用真实路测数据做 AEB 回灌对比验证
- "最大挑战？" → Autosar OS 模块的系统调用和硬件绑定很深，需要逐一做条件编译和平台抽象，最后用 CMake toolchain 管理两套配置
- "代码规模？" → 整个 IFC 算法代码几万行，我负责通信栈和应用层的迁移，加上编译工具链和文档

### 项目 2：多传感器真值采集系统

**一句话概括：** 独立负责多激光雷达、相机、GNSS/IMU 的集成和时间同步，为感知算法评估提供高精度真值数据。

**面试话术：**

> 这个项目是给广汽埃安车型搭建多传感器真值采集系统。我主要负责三块：
>
> 第一，传感器接入。集成了两套激光雷达方案——Pandar128+黑珍珠和速腾128+黑珍珠，覆盖远距离和补盲。设计上用了工厂模式，定义统一的 LidarDriver 接口，不同厂商各自实现，上层算法只依赖接口。
>
> 第二，时间同步。这是最关键的——GNSS 提供 PPS 脉冲做主时钟，激光雷达和相机通过硬件触发线同步曝光，域控通过 PTP 协议同步系统时间，最终授时精度在 1ms 以内。
>
> 第三，交付了高质量的真值数据集，直接用于量产车感知算法的性能评估。
>
> 这个经验对 CSDK 开发很直接——SDK 需要对接不同机型的传感器，硬件抽象和时间同步是核心能力。

**可能的追问：**

- "不同厂商激光雷达的差异？" → 扫描线数、分辨率、点云密度、UDP 数据包格式都不一样，但通过统一接口抽象后上层无感
- "时间同步精度怎么验证？" → 用示波器测 PPS 脉冲和传感器曝光信号的时延

### 项目 3：HIL 自动化测试框架（展示架构能力）

**一句话概括：** 主导开发了支撑 36 万条用例、14 个业务域、23 套车型配置的 HIL 自动化测试平台。

**面试话术：**

> 这个项目规模比较大，13 万行 Python。我主要做架构设计：
>
> 第一，服务端-客户端分离。FastAPI 服务端常驻管理底盘仿真和时间同步资源，客户端专注用例调度，避免每次用例都重启仿真环境。这个思路和 SDK 的"连接管理 + 业务调用"分离是一样的。
>
> 第二，用例编排引擎。用 CSV/JSON 驱动，支持分组执行、增量回归、参数拼装。我把用例调度和配置抽象为配置层，用例工程师不需要写调度代码。
>
> 第三，多车型适配。用 conftest 模式，每车型一份 conftest 管理夹具和配置，新车型接入只需新增配置，不改框架代码。23 套车型配置、6 个芯片平台，接入成本很低。
>
> 第四，CI/CD 流水线。维护 12 stage 的 GitLab CI，支撑日均 30+ 条 Pipeline、300+ 个 Job，成功率 93%+。

**可能的追问：**

- "36 万条用例怎么管？" → CSV/JSON 驱动的编排引擎，分类、分组、按场景调度
- "Pipeline 失败了怎么排查？" → 监控看板系统，11 个 Grafana Dashboard 按角色分层，运维看资源、开发看失败根因、TL 看趋势

---

## 五、简历算法点防深挖（简历上写了算法词，面试官可能追问）

### 真值系统 — 多传感器时间同步

**"PTP 和 PPS 是什么？怎么做到 <1ms 的？"**

> PPS（Pulse Per Second）是 GNSS 接收器每秒发出的一个硬件脉冲信号，精度在纳秒级，作为系统的绝对时钟基准。PTP（Precision Time Protocol）是网络时间同步协议，域控通过 PTP 和 GNSS 主机同步系统时间。
>
> 具体做法：GNSS 输出 PPS 脉冲给激光雷达和相机做硬件触发，保证它们在同一时刻曝光/扫描。域控通过 PTP 协议把自己的系统时钟和 GNSS 对齐。最终授时精度 <1ms，用示波器测 PPS 脉冲和传感器曝光信号的时延来验证。

**"为什么需要时间同步？"**

> 多传感器融合的前提是数据对齐。比如激光雷达 10Hz、相机 30Hz、IMU 200Hz，不做时间同步的话，算法拿到的点云和图像可能差了 50ms——车速 60km/h 时 50ms 就是 0.8 米的位置偏差，感知结果直接错位。

### 真值系统 — 多激光雷达方案

**"Pandar128 和速腾 128 有什么区别？为什么用两套？"**

> 两套是给不同车型用的，不是同时装。Pandar128 是禾赛的，速腾 128 是速腾聚创的，都是 128 线机械旋转式激光雷达。区别主要在点云密度、UDP 数据包格式、驱动 SDK 接口。我设计时做了统一抽象——定义 LidarDriver 接口，两套方案各自实现，上层算法不感知差异。
>
> 黑珍珠是补盲雷达，线数少但覆盖近场盲区，和主雷达互补。

### 智能垃圾桶 — 深度学习模型

**"用了什么模型？怎么训练的？"**

> 用百度 PaddlePaddle 框架做的图像分类。数据集是自己收集的——拍了不同角度、不同光照下的常见垃圾照片，标注了可回收/不可回收/厨余/有害四类。模型选的是轻量级分类网络（MobileNet 级别），因为要在树莓派上实时推理。
>
> 树莓派上部署的挑战是算力有限，做了模型量化和输入尺寸裁剪来加速。STM32 通过串口和树莓派通信，负责传感器采集和电机控制。

**追问："为什么不用 YOLO 做检测？"**

> 场景是垃圾桶内部固定视角，垃圾一件一件投放，不需要定位，分类就够了。分类模型比检测模型轻得多，树莓派上帧率更高。如果场景变成"垃圾桶周围地上有没有垃圾"，那才需要检测。

### 自主学习 — Transformer / LoRA / DPO / GRPO

**"你简历里写了这些，学到什么程度？"**

> 我系统学过 Transformer 架构——Self-Attention 的 QKV 计算、Multi-Head 并行、位置编码的作用。LoRA 是低秩适配，在原始权重旁加两个小矩阵 AB 做微调，只更新 AB 不动原始权重，参数量减少 90% 以上。DPO 是直接偏好优化，不需要训 reward model，直接用偏好数据对做对比学习。GRPO 是分组相对策略优化，DeepSeek-R1 用的方法，用组内相对排名替代 Critic 网络。
>
> 学这些主要是为了理解大模型怎么训练和微调——虽然 CSDK 不直接写模型，但 SDK 需要支撑模型部署，了解模型结构和推理优化有助于设计更好的 API 和部署方案。

### 自主学习 — 强化学习 / MPC / VLA

**"PPO 和 MPC 有什么区别？为什么都学？"**

> PPO 是数据驱动，从零学习策略，不需要环境模型，但需要大量试错。MPC 是模型驱动，需要精确的系统动力学模型，在线滚动优化，能处理约束。两者互补——MPC 做安全约束层保证不越界，学习策略做任务级决策。无人机上典型做法是：PPO/SAC 学出高层策略，底层用 MPC 或 PID 保证安全执行。

**"为什么关注 VLA？"**

> VLA 是具身智能的核心范式，把视觉理解和动作生成统一到一个模型里。我关注它是因为 SDK 未来需要支撑这种端到端模型的部署——模型推理延迟、模型更新机制、Sim2Real 迁移，这些都对 SDK 的架构有要求。

---

## 六、算法基础速成（JD 要求了解，能说 1-2 分钟即可）

> 策略：SDK 岗不要求写算法，但要能讲清楚"这些算法是干什么的，SDK 怎么支撑它们"

### 卡尔曼滤波（传感器融合基础）

**一句话：** 把多个传感器的测量值融合成一个更准确的估计。

**两句话就能讲清楚：** "预测 + 更新"两步循环。预测步用运动模型推算下一时刻状态，更新步用传感器测量值修正预测。自动驾驶里 GPS 低频但绝对位置准，IMU 高频但会漂移，卡尔曼滤波把两者结合，得到高频且准确的定位。

**SDK 视角：** CSDK 需要给算法提供**时间戳对齐**的多传感器数据，这是融合的前提。

### 路径规划（A* / RRT）

**A\*：** 已知地图上找最短路径。维护 open list（待探索）和 closed list（已探索），每次选 f(n) = g(n) + h(n) 最小的节点扩展。h(n) 是启发函数，不高于实际距离就能保证最优解。

**RRT（Rapidly-exploring Random Tree，快速探索随机树）：** 高维空间、未知环境。从起点随机采样、向随机方向延伸、碰撞检测，直到连到目标。适合无人机这种高自由度场景。

**一句话记忆：** A\* 适合已知地图最短路径，RRT 适合未知/高维空间。

### SLAM（同时定位与建图）

**一句话：** 没有 GPS 时，一边建地图一边定位自己。

- **前端做特征提取和帧间匹配（视觉 SLAM 用 ORB 特征点，激光 SLAM 用 ICP 点云匹配），产生粗略位姿**。
- **后端做全局优化消除累积误差，回环检测修正漂移。** 无人机室内飞行、自动驾驶地下车库都依赖 SLAM。

### PID 控制

**一句话：** 最经典的控制算法，根据误差的比例(P)、积分(I)、微分(D)调整输出。

```
u(t) = Kp*e(t)  +  Ki*∫e(t)dt  +  Kd*de(t)/dt
        比例(现在)    积分(过去累积)     微分(未来趋势)
```

| 项   | 作用   | 问题     |
| --- | ---- | ------ |
| P   | 快速响应 | 有余差    |
| I   | 消除静差 | 可能超调振荡 |
| D   | 抑制超调 | 对噪声敏感  |

**无人机应用：** 姿态控制全是 PID 回路——期望角度和当前角度的偏差输入，输出电机转速指令。

### 深度学习感知（目标检测/分割）

自动驾驶感知用 CNN/Transformer 做目标检测（YOLO）和语义分割。激光雷达点云用 PointPillars/CenterPoint 做 3D 检测。**对 SDK 的要求：** 低延迟传输大块数据（点云、图像），时间戳精确同步。

### 强化学习（PPO / SAC）

- **PPO（Proximal Policy Optimization，近端策略优化）**：on-policy，更新时限制策略变化幅度防止训练崩溃，**稳定但需要大量采样**
- **SAC（Soft Actor-Critic，柔性演员-评论家）**：off-policy，样本效率高。Actor 输出动作，Critic 评价动作好坏。**Soft** 指加入最大熵目标——不是贪婪选 Q 值最大的动作，而是鼓励探索、保持随机性，避免过早收敛到局部最优。适合真实机器人（数据珍贵）
- 训练在仿真器里大规模并行，训练完导出 ONNX 部署到嵌入式设备

**on-policy vs off-policy：**

|       | on-policy（PPO）     | off-policy（SAC）            |
| ----- | ------------------ | -------------------------- |
| 训练数据  | **必须当前策略新采的，用完就扔** | **历史数据存 replay buffer 复用** |
| 数据利用率 | 低                  | 高                          |
| 稳定性   | 更稳定                | 需额外技术防过估计                  |
| 适用场景  | 仿真环境（可大量并行）        | 真实机器人（数据贵）                 |

**价值估计方法：MC vs TD vs GAE（PPO 实际用的是 GAE）：**

```
MC（蒙特卡洛）：跑完一整个 episode，用实际回报累加
  V(s_t) ≈ r_t + r_t+1 + ... + r_T
  优点：无偏   缺点：方差大，必须等到 episode 结束

TD（时序差分）：走一步就能更新，用当前奖励 + 下一状态估计值
  V(s_t) ≈ r_t + γ·V(s_t+1)
  优点：方差小，在线更新   缺点：有偏（V(s_t+1) 本身不准确）
```

**GAE（广义优势估计）：** MC 和 TD 的折中。不等到 episode 结束，也不只看一步，而是**指数加权平均不同步数的估计**，用参数 λ 控制偏向：

| λ 值 | 退化为 | 特点 |
|---|---|---|
| λ=0 | TD(0) | 只看一步，方差小但有偏 |
| λ=1 | MC | 看到结束，无偏但方差大 |
| 0<λ<1 | GAE | 折中，越远的步权重越小 |

**一句话：** PPO 采样用当前策略跑几帧，价值估计用 GAE（MC 和 TD 的混合），不是纯蒙特卡洛。纯 MC 在机器人任务中方差太大，几乎不用。

### VLA（视觉-语言-动作模型）

机器人领域核心范式：输入图像+语言指令，直接输出动作（关节角度、末端位姿）。代表工作 RT-2、π0、OpenVLA。最大瓶颈是推理延迟（7B 模型 100-500ms），需要量化/TensorRT 加速才能部署到边缘端。

### 面试话术：SDK 怎么支撑这些算法

> CSDK 是算法和硬件之间的桥梁。对感知算法，SDK 负责把原始传感器数据高效传输给算法模块，保证时间戳对齐；对控制算法，SDK 负责把算法输出的指令编码为 MAVLink/CAN 协议下发到飞控；对规划算法，SDK 提供飞控状态的实时订阅。SDK 不是写算法，而是让算法能**高效、可靠地跑起来**。

---

## 七、无人机/飞控速成知识（能说 2-3 分钟即可）

### MAVLink 协议

> MAVLink 是无人机通信的事实标准，轻量级的消息协议。它定义了标准消息——心跳、GPS 位置、姿态、控制指令、任务等。CSDK 底层就是通过串口或 UDP 收发 MAVLink 包，上层封装为友好的 API。

记住一句话：**MAVLink 就是无人机领域的 ROS topic，轻量级的发布订阅。**

### PX4 飞控架构

> PX4 内部用 uORB 消息总线做模块间通信，和 Autosar 的 RTE 层很像。核心模块包括 commander（状态机）、navigator（航点执行）、姿态/位置控制器。CSDK 通过 MAVLink 接入这个总线，读取飞控数据、下发控制指令。

记住一句话：**PX4 的 uORB 消息总线 ≈ Autosar 的 RTE 层，都是模块间异步通信中间件。**

### 无人机 SDK 典型功能

- 连接管理（串口/UDP/4G）
- 航点飞行（上传、执行、暂停、恢复）
- 云台/相机控制
- 遥测订阅（位置、姿态、电量、速度）
- 返航、降落、紧急停桨

---

## 八、系统设计题："设计一个无人机 SDK"

如果面试官问"从零设计一个无人机航点飞行 SDK，你怎么做？"

**答法（3 分钟版本）：**

> 我分三层来设计：
>
> **底层通信层：** 负责 MAVLink 协议的编解码和连接管理。支持串口、UDP、4G 多种连接方式。心跳机制维持连接，超时断开自动重连。
>
> **核心服务层：** 这是 SDK 的核心逻辑。
> - 命令队列：所有控制指令排队发送，支持优先级（紧急停桨 > 航点 > 云台控制）
> - 状态同步：飞控的遥测数据通过回调推送给上层，支持按频率订阅
> - 超时和重试：每条指令有超时时间，超时自动重试，达到上限通知上层
> - 任务状态机：航点任务的状态流转（就绪→上传→执行→暂停→恢复→完成→失败）
>
> **接口层：** 提供两套 API。
> - 同步 API：适合简单场景，每个调用阻塞等待结果
> - 异步 API：适合复杂场景，回调/future/协程三种模式可选
>
> **向下兼容性：** 这是 SDK 开发的难点。API 版本号管理，废弃接口用 deprecated 标记给用户迁移时间，不随意删除已有接口。用 pimpl 模式隐藏实现细节，保证 ABI 兼容。
>
> 这个设计思路来自我在 HIL 框架和 Autosar 迁移中的经验——分层架构、接口抽象、向下兼容。

---

## 九、高频行为问题

**Q: "你最近两年主要写 Python，C++ 还熟吗？"**

> 我在禾多做了 3 年纯 C++ 开发——传感器驱动、Autosar 迁移、CAN 通信、Linux 多线程，都是底层 C++ 项目。到元戎后虽然主力语言是 Python，但 HIL 框架的架构设计方法论是通用的。而且我一直在自学 C++20 的新特性，比如协程和 Asio 异步编程。我最近的笔记就是 C++20 协程重写 Asio 代理。写代码的话，C++ 的手感还在，需要的话我可以很快捡回来。

**Q: "你做过的是测试，和 SDK 开发有什么关系？"**

> 我做的不是纯测试，是测试平台开发，本质上是做系统架构和工程化。IFC SIL 项目更是直接做 SDK——把 Autosar 算法从特定硬件上解耦，提供 x86 平台可调用的模块化接口。这和 CSDK "向下屏蔽硬件差异、向上提供统一 API" 的目标完全一致。HIL 框架的多车型适配也是用策略模式做抽象，新车型接入不改框架代码，这和 SDK 的多平台兼容性是一个问题。

**Q: "你没有无人机经验，怎么弥补？"**

> 第一，自动驾驶和无人机在底层技术上高度相通——传感器、CAN/MAVLink 通信协议、实时系统、时间同步，这些我都有实战经验。第二，我对新领域的学习速度很快，之前在禾多从传感器应用切换到 SIL 集成开发，一个月就独立负责项目了。第三，我一直在自学机器人相关的内容，包括 Isaac Lab 仿真、强化学习、Sim2Real 部署，对无人机方向的算法和工程都有基础了解。

---

## 十、反问面试官的问题（展示你的深度）

面试官问"你有什么想问的？"时，选 2-3 个：

1. "CSDK 目前主要支持哪些机型？不同机型之间 API 的差异大吗？是怎么做兼容性管理的？"
2. "SDK 团队和飞控团队、算法团队的协作模式是什么样的？接口设计决策的流程是什么？"
3. "目前 CSDK 的性能瓶颈在哪里？是通信延迟、序列化/反序列化，还是飞控本身的响应速度？"
4. "团队目前 SDK 的规模大概是多大？用 C++ 哪个版本？构建系统用什么？"

---

## 十一、明天时间安排

| 时间             | 内容                         | 目标             |
| -------------- | -------------------------- | -------------- |
| 上午 9:00-11:00  | 过一遍 C++ 20 题，每题口头讲出来       | 能流利回答，不卡壳      |
| 上午 11:00-12:00 | 手写 6 道代码题（用纸笔！）            | 不用 IDE 也能写出来   |
| 下午 14:00-15:30 | 背 3 个项目话术，每个讲 3 分钟         | 不看稿，自然讲出来      |
| 下午 15:30-16:30 | 看 MAVLink/PX4 速成内容 + 系统设计题 | 能说 2-3 分钟即可    |
| 下午 16:30-17:30 | 休息，不要再学新东西                 | 放空             |
| 晚上 18:00-18:30 | 热身：默念自我介绍 + 项目话术           | 进入状态           |
| 晚上 18:30-19:00 | 检查网络、摄像头、麦克风               | 技术准备           |
| 晚上 19:00       | 面试！                        | 自信、语速适中、不会就说思路 |

---

## 十二、面试当天注意事项

1. **不会的题不要硬编**：说"这块我了解不深，但我可以讲一下我的理解"比胡说好
2. **手撕代码时边写边讲**：解释你的思路，面试官看的是思考过程不只是结果
3. **项目经历不要背稿**：听起来假，用自然的口语讲，重点突出"我做了什么"和"结果怎么样"
4. **语速不要太快**：紧张容易语速加快，有意识地放慢
5. **如果被问到 C++ 细节想不起来**：说"我印象中是这样，但不太确定，原理上应该是..."比直接说"不知道"好
6. **面试结束前确认**：问一下"您对我还有什么想了解的？"或"后续流程大概是什么样的？"