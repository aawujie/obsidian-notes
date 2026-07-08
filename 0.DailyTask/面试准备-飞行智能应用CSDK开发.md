---
share_link: https://share.note.sx/nl8oz7h0#sqnDmv7E9/4yo6Ify+fQGpIs9OYOmljgPoC1NCnFZ6c
share_updated: 2026-07-08T15:20:06+08:00
---
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

## 二、C++ 必考 20 题

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
- 运行速度会大幅变慢（**valgrind 插桩模拟内存管理**），**只用于调试，不用于生产环境**

**"插桩" 怎么理解？**

valgrind 在程序的每一条内存操作指令前后插入监控代码，就像每个内存操作都要过安检：

```
正常程序：malloc → 写 → free → 结束

插桩后：  malloc → [记录：file.c:42 分配了 100 字节]
          *ptr = 42 → [检查：ptr 指向有效内存吗？]
          free → [记录：该内存已释放]
          程序退出 → [遍历记录表：有分配了没释放的吗？]
                   → 输出泄漏报告
```

**为什么慢 10-20 倍？** 原来一条 `mov` 指令就能完成的事，valgrind 要插进去十几条检查指令。每读写一次内存，都要先查表验证"这个地址合法吗？被 free 过了吗？越界了吗？"——这就是插桩的代价。
- 同时还能检测：野指针读写、缓冲区溢出、重复 free、栈溢出等非法内存操作

**Q3: 智能指针怎么选？怎么用？**

```
unique_ptr — 独占所有权，不能拷贝只能移动，开销接近裸指针
shared_ptr — 共享所有权，引用计数（原子操作），有开销
weak_ptr   — 配合 shared_ptr 打破循环引用，不增加引用计数
```

- 默认用 unique_ptr、需要共享才用 shared_ptr

**weak_ptr 什么时候用？打破循环引用，弱引用，不增加引用计数**

两个对象互相持有对方的 shared_ptr 会导致**永远不会释放**：

```cpp
class B;  // 前向声明

class A {
public:
    std::shared_ptr<B> ptr_b;  // A 持有 B
    ~A() { std::cout << "A destroyed" << std::endl; }
};

class B {
public:
    std::shared_ptr<A> ptr_a;  // B 持有 A  ← 循环引用！
    ~B() { std::cout << "B destroyed" << std::endl; }
};

int main() {
    auto a = std::make_shared<A>();
    auto b = std::make_shared<B>();
    a->ptr_b = b;  // a 引用计数 = 1, b 引用计数 = 1
    b->ptr_a = a;  // a 引用计数 = 2, b 引用计数 = 2
    return 0;
    // 离开作用域：a 引用计数 = 1, b 引用计数 = 1
    // 互相持有，永远不会降到 0 → 内存泄漏！析构函数永远不会调用
}
```

**解法：把其中一个换成 weak_ptr：**

```cpp
class B {
public:
    std::weak_ptr<A> ptr_a;  // 弱引用，不增加引用计数
};

// 离开作用域：a 引用计数 → 0, 释放 A → b 引用计数 → 0, 释放 B ✅
```

**weak_ptr 使用方式：** 不能直接访问对象，必须 `lock()` 转为 shared_ptr 后才能用：

```cpp
std::weak_ptr<A> weak_a = ...;
if (auto shared = weak_a.lock()) {  // 如果对象还活着
    shared->doSomething();           // 安全使用
}
// 如果对象已被销毁，lock() 返回 nullptr
```

**典型场景：** 观察者模式（subject 持有 observer 的 weak_ptr）、树结构（子节点用 shared_ptr 指向父节点时用 weak_ptr）、缓存（weak_ptr 不阻止缓存被清理）。

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

**基本机制：**

- 每个有虚函数的类有**一张** vtable，存在**只读数据段**（`.rodata`），编译期生成
- 每个对象有**一个** vptr（**8 字节，64 位系统**），指向所在类的 vtable
- 调用虚函数时：`obj->vptr[vtable_index]()` → 查表 → 跳转，比直接调用多一次间接寻址

**为什么虚函数必须存在 vtable 里？**

根本原因是**编译期不知道运行时对象的实际类型，无法在编译期确定指令地址**：

```cpp
class Base {
public:
    virtual void foo() { ... }
};
class DerivedA : public Base {
public:
    void foo() override { ... }  // 行为 A
};
class DerivedB : public Base {
public:
    void foo() override { ... }  // 行为 B
};

void process(Base* p) {
    p->foo();  // ← p 可能是 Base、DerivedA 或 DerivedB，编译期无法决定
}
```

编译器看到 `p->foo()` 时，**只知道 `p` 的静态类型是 `Base*`**，但 **`process` 可能被传入任何派生类对象**。编译器不可能在编译期穷举所有可能的类型。vtable 的解决方案是**把"调哪个函数"这个决策推迟到运行时——每个对象自带 vptr 指向正确的 vtable**，运行时查表跳转。

**内存布局（以单继承为例）：**

```
Base 对象                          Base vtable
┌──────────────┐                  ┌────────────┐
│  vptr ───────┼─────────────────→│ Base::f1   │
│  成员变量1    │                  │ Base::f2   │
│  成员变量2    │                  │ Base::~B   │
└──────────────┘                  └────────────┘


Derived 对象                       Derived vtable
┌──────────────┐                  ┌─────────────────────┐
│  vptr ───────┼─────────────────→│ &Derived::func1()    │ ← 覆盖
│  成员变量1    │                  │ &Base::func2()       │ ← 保留基类
│  成员变量2    │                  │ &Derived::~Derived() │ ← 覆盖
└──────────────┘                  └─────────────────────┘
```

**关键：** 一个对象只有一个 vptr，指向一个 vtable。Base 对象指向 Base 的 vtable，Derived 对象指向 Derived 的 vtable。Derived 的 vtable 里，被重写的函数替换为自己的地址，没重写的保留基类地址。

**构造函数中 vptr 的逐级设置：**

```cpp
class Base {
public:
    Base() { foo(); }        // 构造时调虚函数
    virtual void foo() { cout << "Base::foo" << endl; }
};
class Derived : public Base {
public:
    Derived() { foo(); }
    virtual void foo() override { cout << "Derived::foo" << endl; }
};

Derived d;  // 输出：Base::foo  然后  Derived::foo
// 不是两个 Derived::foo！
```

**为什么 vptr 要逐级设置？这是安全机制，不是多此一举：**

```cpp
class Base {
public:
    Base() { foo(); }
    virtual void foo() { cout << "Base::foo" << endl; }
};

class Derived : public Base {
    int* data_;  // 还没初始化！
public:
    Derived() : data_(new int(42)) {  // ← 这个要在 Base() 之后才执行
        foo();
    }
    void foo() override {
        *data_ = 10;  // 如果 Base() 时调了这行，data_ 还是野指针，直接崩！
    }
};
```

**构造顺序是基类先、派生类后。** 在 `Base()` 执行期间，**`Derived` 的成员变量 `data_` 还没初始化**。如果 vptr 一上来就指向 `Derived` 的 vtable，`Base()` 里调 `foo()` 就会查到 `Derived::foo()` → 访问未初始化的 `data_` → **崩溃**。

**C++ 的设计：** 在 `Base()` 执行期间，vptr 指向 `Base` 的 vtable，保证调不到派生类成员。`Base()` 结束 → 派生类成员初始化完成 → vptr 更新为 `Derived` 的 vtable → 进入 `Derived()` 构造函数 → 此时所有成员已初始化，安全。

**多继承下的 vtable：**

```cpp
class Derived : public Base1, public Base2 { ... };
```

对象有**多个 vptr**——每个基类一个，按声明顺序堆叠。**内存布局：**

```
Derived 对象                         vtables
┌──────────────┐
│  vptr_Base1 ─┼─────────────→ vtable_for_Base1
│  Base1 成员   │              ┌──────────────────────┐
│  vptr_Base2 ─┼──────┐       │ &Derived::func1()     │
│  Base2 成员   │      │       │ &Base1::func2()       │
│  Derived 成员 │      │       └──────────────────────┘
└──────────────┘      │
                      └───→ vtable_for_Base2
                           ┌──────────────────────┐
                           │ &Derived::func3()     │
                           │ &Base2::func4()       │
                           └──────────────────────┘
```

**调用 `Base2*` 指针的虚函数时，需要先调整 this 指针（偏移到 Base2 子对象），再查 vtable**。这就是为什么 `static_cast` 和 `dynamic_cast` 在多继承下开销不同。

**虚继承（virtual inheritance）下的 vtable：**

菱形继承问题——不用虚继承，`Base` 会重复两份：

```
  A（基类）
 / \
B   C
 \ /
  D（最终派生类）

不用虚继承 → D 里有两份 A，调用 A::foo() 有歧义
用了虚继承 → D 里只有一份 A
```

虚继承引入**虚基类表**（vbtable），存虚基类子对象的偏移量：

```
Derived 对象
┌──────────────┐
│  vptr_Derived┼──→ vbtable                ┌───────────────┐
│  Derived 成员 │    │ offset_to_Base       │  ← 存偏移量    │
│              │    └───────────────┘
│  vptr_Base   ┼──→ vtable（共享的 Base）    ┌────────────┐
│  Base 成员   │    │ Base::f1  Base::~B    │  ← 存函数指针  │
└──────────────┘    └────────────┘
```

**关键：** vbtable 和 vtable 是不同的东西。vtable 存函数指针（调哪个函数），vbtable 存偏移量（虚基类在哪）。调用虚基类成员时，先查 vbtable 找到偏移量，再跳过去。多了一次间接寻址，比普通继承慢一点，但解决了菱形继承的重复问题。

**性能开销：**

| 开销类型 | 来源                                   | 代价  |
| ---- | ------------------------------------ | --- |
| 空间   | 每个对象多 8 字节 vptr，每类多一张 vtable         | 小   |
| 时间   | 虚函数调用多一次间接寻址（查 vptr → 查 vtable → 跳转） | 微小  |
| 内联损失 | 编译器无法内联虚函数（除非能确定静态类型）                | 可能大 |
| 分支预测 | 虚函数调用是间接跳转，CPU 难以预测                  | 可能大 |

**什么情况下不用虚函数：** 热点循环中频繁调用的函数、确定不需要多态的函数、**模板可以替代的场景**（CRTP——奇异递归模板模式，**编译期多态零开销**）。

**纯虚函数与抽象类：**

```cpp
class Abstract {
public:
    virtual void func() = 0;  // 纯虚函数，vtable 里对应槽位填 NULL
};
// Abstract a;  // ❌ 不能实例化，因为 vtable 不完整
```

纯虚函数在 vtable 中对应 **`__cxa_pure_virtual`**（GCC）或 **`_purecall`**（MSVC），如果意外调用会触发运行时错误。

**构造函数/析构函数中为什么不能调虚函数？**

**构造函数：vptr 还没设置完**，此时调虚函数不会多态，**调的是当前构造阶段的版本。**
**析构函数：vptr 已退化到当前析构阶段**，**派生类对象已被销毁**，调虚函数也不会多态。

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

**std::move 的本质：只是类型转换，真正转移资源的是移动构造函数**

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

`forward` 底层就是 `static_cast`，关键是模板参数 T 携带了 "原始值是左值还是右值" 的信息：

```cpp
// forward 简化实现
template<typename T>
T&& forward(remove_reference_t<T>& arg) noexcept {
    return static_cast<T&&>(arg);
}
```

| 调用                     | T 推导为  | `T&&` 折叠后        | forward 返回 |     |
| ---------------------- | ------ | ---------------- | ---------- | --- |
| `wrapper(a)` (a 是左值)   | `int&` | `int& && → int&` | 左值         |     |
| `wrapper(10)` (10 是右值) | `int`  | `int&&`          | 右值         |     |

**引用折叠规则：** 只有一条——**只要有左值引用 `&` 参与，结果就是左值引用。**

```
&  + &  → &       左值 + 左值 → 左值
&  + && → &       左值 + 右值 → 左值 （& 赢）
&& + &  → &       右值 + 左值 → 左值 （& 赢）
&& + && → &&      只有全右值，才保持右值
```

**为什么需要这个规则？** 模板里 `T&&` 是万能引用，`T` 可能推导为 `int&` 或 `int`：

```cpp
template<typename T>
void wrapper(T&& arg) { ... }

int a = 10;
wrapper(a);          // T = int&，  T&& = int& && → int&
wrapper(10);         // T = int，   T&& = int&&
```

**一句话对比：** move 和 forward 底层都是 `static_cast`，区别在于 move 无条件转右值，forward 通过模板推导决定是否转右值。

**Q9: 左值和右值怎么区分？**

- 简单判断：**能取地址（&x）的是左值，不能的是右值**
- 左值：**有名字的变量、可以出现在赋值号左边**
- 右值：**字面量、临时对象、move 的结果**

**三类右值的存放位置（面试加分项）：**

| 右值类型                 | 存放位置              | 特点                         |
| -------------------- | ----------------- | -------------------------- |
| 字面量（`42`、`"hello"`）  | **代码段 `.rodata`** | 编译期确定，只读，程序运行全程存在          |
| 临时对象（`a+b`、函数返回的临时值） | **栈（或寄存器）**       | **表达式结束后立即析构**，编译器会 RVO 优化 |
| move 的结果             | **堆（接管原对象资源）**    | **move 本身不分配内存，只是指针转移**    |

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

**不会报错，但内容是空的。** 被 move 的对象处于 **"有效但未指定"（valid but unspecified）状态**：

```cpp
std::string s1 = "hello";
std::string s2 = std::move(s1);

std::cout << s1;        // 输出空字符串 ""，不会崩溃
std::cout << s1.size(); // 输出 0
s1 = "world";           // ✅ 可以重新赋值，继续正常使用
```

- **标准库类型**（`string`、`vector`、`unique_ptr`）：**move 后保证合法**——**string/vector 变空，unique_ptr 变 nullptr**
- **自己写的类**：**移动构造函数里必须把原对象的指针置空（`other.ptr_ = nullptr`），否则析构时 double free**
- 关键原则：move 后可以调用**没有前置条件**的方法（`.empty()`、赋值），但不能假设数据还在

**什么场景会 move？**

```cpp
// 1. 放入容器，避免第二次深拷贝
std::string s = "very long string...";// 第一次复制（.rodata → 堆，不可避免）
vec.push_back(std::move(s));      // 省掉第二次复制（堆 → 新堆），O(1) 偷指针

// 2. 转移所有权（unique_ptr 只能 move 不能 copy）
std::unique_ptr<Foo> p2 = std::move(p1);  // p1 变 nullptr

// 3. 高效的 swap（内部就是 move）
std::swap(a, b);  // 只交换指针，不拷贝内容

// 4. 把对象交给另一个线程
std::thread t([data = std::move(data)] { process(data); });
```

**一句话：** 只要对象后面不再需要了，就 move——省一次深拷贝。**`string`/`vector` move 是 O(1)（偷指针），拷贝是 O(n)（复制全部数据）。**

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

**`constexpr` 函数不是 "必须编译期执行"：**

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

**`const` 成员函数：承诺不修改成员变量**

**const 对象只能调 const 成员函数**

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

|       | `const` 成员函数         | `constexpr` 函数  |     |
| ----- | -------------------- | --------------- | --- |
| 修饰什么  | **函数行为（承诺不改成员）**     | 返回值（可以编译期求值）    |     |
| 能用于   | 只能成员函数               | 成员函数、普通函数都可以    |     |
| 关键作用  | const 对象只能调 const 函数 | 返回值可以当数组大小、模板参数 |     |
| 修饰返回值 | 语义不同，很少用             | —               |     |

**const 修饰返回值（很少用，只有返回引用/指针时才有意义）**

```cpp
// const 修饰返回值（很少用，只有返回引用/指针时才有意义）
const int  foo() { return 5; }       // 没意义，调用者拿的是拷贝
const std::string& getName() const;  // 有意义，防止调用者修改内部数据
```

**C++14/17 新特性（面试可能问，知道这些就够了）：**

C++14 重点：
- `auto` 返回值推导：函数返回值可以直接写 `auto`，编译器自动推导
- 泛型 lambda：`[](auto x, auto y) { return x + y; }`，参数类型自动推导
- `std::make_unique<T>()`：创建 unique_ptr，比 `new` 更安全
- `constexpr` 放宽：函数内可以有循环和分支（文档 Q11 里 factorial 就是 C++14 特性）

C++17 重点：
- `if constexpr`：编译期 if，不符合条件的分支不会编译，结合 traits 做条件编译比 `enable_if` 简洁得多
- 结构化绑定：`auto [x, y, z] = getPoint();` 一行拆解 tuple/struct
- `std::optional<T>`：可能没有值的返回值，避免用空指针或 -1 表示"没有"
- `std::string_view`：字符串的只读视图，不拷贝，传参高效
- `std::variant<T1, T2, ...>`：类型安全的 union，存多个类型中的一个
- `[[nodiscard]]`：标记返回值不应被忽略，编译器会警告
- CTAD（类模板参数推导）：`std::pair p(1, 2.0);` 不用写 `std::pair<int, double>`

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

死锁四个条件：**互斥、持有等待、不可剥夺、循环等待**。打破任意一个就不会死锁：

**1. 固定加锁顺序（打破循环等待）**

```cpp
std::mutex a, b;

// ❌ 死锁：线程1 先锁 a 再 b，线程2 先锁 b 再 a → 循环等待
void thread1() { std::lock_guard lk1(a); std::lock_guard lk2(b); }
void thread2() { std::lock_guard lk1(b); std::lock_guard lk2(a); }

// ✅ 所有线程都先锁 a 再锁 b，顺序一致，不会形成环
```

**2. std::lock() 同时锁（打破持有等待）**

```cpp
// ✅ 一次拿所有锁，拿不到就全释放重试，不"持 A 等 B"
std::lock(a, b);
std::lock_guard lk1(a, std::adopt_lock);  // adopt_lock：接管，不重复加锁
std::lock_guard lk2(b, std::adopt_lock);
```

**3. try_lock 超时放弃（打破不可剥夺）**

```cpp
std::timed_mutex a, b;

if (a.try_lock_for(std::chrono::milliseconds(100))) {
    if (b.try_lock_for(std::chrono::milliseconds(100))) {
        std::lock_guard lk1(a, std::adopt_lock);
        std::lock_guard lk2(b, std::adopt_lock);
        return;
    }
    a.unlock();  // 拿到 a 但拿不到 b，释放 a
}
```

**优先顺序：** `std::lock()` > 固定顺序 > `try_lock`。

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

**一句话：** C++11 把 **"双检查锁"（DCLP）的坑由编译器帮你填了**，用函数内 static 变量就是最简单、最安全、最高效的单例写法。

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

**Q21: C++ 有哪几种构造函数？**

```cpp
class Foo {
    int val_;
    int* data_;
public:
    // 1. 默认构造函数
    Foo() : val_(0), data_(nullptr) {}

    // 2. 带参构造函数
    Foo(int v) : val_(v), data_(new int(v)) {}

    // 3. 拷贝构造函数（const 左值引用）
    Foo(const Foo& other) : val_(other.val_), data_(new int(*other.data_)) {}

    // 4. 移动构造函数（右值引用，noexcept）
    Foo(Foo&& other) noexcept : val_(other.val_), data_(other.data_) {
        other.data_ = nullptr;
    }

    // 5. 委托构造函数（C++11，调另一个构造函数）
    Foo(double v) : Foo(static_cast<int>(v)) {}

    ~Foo() { delete data_; }
};
```

| 构造函数                                               | 签名                        | 何时调用                     |
| -------------------------------------------------- | ------------------------- | ------------------------ |
| 默认                                                 | `Foo()`                   | `Foo f;`                 |
| 带参                                                 | `Foo(int)`                | `Foo f(42);`             |
| 拷贝                                                 | `Foo(const Foo&)`         | `Foo f2(f1);`            |
| **<span style="color:rgb(255, 77, 77)">移动</span>** | **`Foo(Foo&&)` noexcept** | `Foo f2(std::move(f1));` |
| 委托                                                 | 调用同类另一个构造函数               | 减少重复代码                   |

**特殊规则：**
- 定义了任何构造函数，编译器就不再生成默认构造函数
- **移动构造应标记 `noexcept`，否则 `vector` 扩容时走拷贝而不是移动**
-  = default 显式要求编译器生成，= delete 禁止使用

**Q22: 移动构造为什么必须加 noexcept？**

**`noexcept` 承诺函数不抛异常**。移动构造不加 `noexcept` 的后果：**vector 扩容时回退到拷贝，不走移动。**

```cpp
// ❌ 没加 noexcept
Foo(Foo&& other) : data_(other.data_) { other.data_ = nullptr; }

// ✅ 加了 noexcept
Foo(Foo&& other) noexcept : data_(other.data_) { other.data_ = nullptr; }
```

**为什么？** vector 扩容时把旧元素移动到新内存。**如果移动中抛异常，旧内存已释放、新内存没建好，数据丢失。** vector 的保守策略：移动构造没加 noexcept → 回退到拷贝（拷贝失败不影响原数据，安全但慢）。

```cpp
std::vector<Foo> v;
v.push_back(Foo());  // 扩容时：
// 有 noexcept → 移动，O(1) 偷指针
// 无 noexcept → 拷贝，O(n) 全量复制
```

**什么时候加 noexcept：** **移动构造/移动赋值（必须加）**、**析构（默认 noexcept）**、**swap（只交换指针）**。

**自己写类时怎么设计 noexcept：**

```cpp
class MyClass {
    int* data_;
    std::string name_;  // string 移动是 noexcept，没问题
    size_t size_;
public:
    // ✅ 只做指针赋值和基础类型赋值，不会抛异常
    MyClass(MyClass&& other) noexcept
        : data_(other.data_)
        , name_(std::move(other.name_))
        , size_(other.size_)
    {
        other.data_ = nullptr;
        other.size_ = 0;
    }
};
```

**如果成员不确定是否 noexcept，用 `std::move_if_noexcept` 兜底：**

```cpp
SafeClass(SafeClass&& other) noexcept
    : data_(std::move_if_noexcept(other.data_))   // 有 noexcept → 移动
    , name_(std::move_if_noexcept(other.name_))   // 无 noexcept → 拷贝
{}
```

**设计原则：**
1. 成员尽量用标准库类型（`string`/`vector`/`unique_ptr`），它们的**移动都是 noexcept**
2. 移动构造里只做指针赋值、`int`/`size_t` 赋值、`swap`，不调 `new`
3. 不确定的成员用 **`std::move_if_noexcept` 自动回退到拷贝**
4. **noexcept 不加 = 白写移动构造，乱加 = 异常来时直接 `std::terminate` 崩掉**

**什么是"乱加"？标了 noexcept 但实际可能抛异常：**

```cpp
// ❌ 乱加：push_back 可能抛 std::bad_alloc
BadMove(BadMove&& other) noexcept
    : data_(std::move(other.data_))
{
    data_.push_back(42);  // ❌ 内存不足 → terminate，不给你 catch 机会
}

// ❌ 乱加：new 可能抛 std::bad_alloc
BadMove2(BadMove2&& other) noexcept {
    data_ = new int(42);  // ❌ 内存不足 → terminate
}

// ✅ 正确：只做指针赋值和基础类型赋值
GoodMove(GoodMove&& other) noexcept
    : data_(other.data_), size_(other.size_)
{
    other.data_ = nullptr;
    other.size_ = 0;
}
```

<span style="color:rgb(255, 77, 77)"><b>能抛异常的操作（不能放 noexcept 里）：</b></span> `new`/`malloc`、`push_back`、调非 noexcept 函数、IO 操作。

<span style="color:rgb(255, 77, 77)"><b>安全操作（可以放 noexcept 里）：</b></span> 指针赋值、`int`/`size_t` 赋值、`swap`、标准库 noexcept 函数。

---

## 三、设计模式

### 单例模式（Singleton）

**用途：** 全局唯一实例，如配置管理器、连接池、日志系统。

**C++11 最简线程安全实现：**

```cpp
class Singleton {
public:
    static Singleton& getInstance() {
        static Singleton instance;  // C++11 保证线程安全初始化
        return instance;
    }
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
private:
    Singleton() = default;
};
```

**你的项目：** HIL 监控看板的配置管理器、全局资源管理器。

### 工厂模式（Factory）

**用途：** 把对象创建逻辑封装起来，调用者不需要知道具体类型。

```cpp
// 定义统一接口
class LidarDriver {
public:
    virtual void start() = 0;
    virtual PointCloud getPointCloud() = 0;
    virtual ~LidarDriver() = default;
};

// 各厂商实现
class Pandar128Driver : public LidarDriver { ... };
class RS128Driver : public LidarDriver { ... };

// 工厂：根据配置创建对应的驱动
std::unique_ptr<LidarDriver> createLidar(const std::string& model) {
    if (model == "Pandar128") return std::make_unique<Pandar128Driver>();
    if (model == "RS128")     return std::make_unique<RS128Driver>();
    throw std::runtime_error("Unknown lidar model");
}
```

**你的项目：** 真值系统中两套激光雷达方案（Pandar128 + 黑珍珠 / 速腾128 + 黑珍珠），定义统一 `LidarDriver` 接口，上层算法不感知底层厂商差异。CSDK 做多机型适配也是这个思路——工厂模式 + 接口抽象。

### 策略模式（Strategy）

**用途：** 同一行为有多种实现，运行时切换。消除 if-else/switch 分支。

```cpp
// 策略接口
class ChassisStrategy {
public:
    virtual void sendControl(const ControlCmd& cmd) = 0;
    virtual ~ChassisStrategy() = default;
};

// 不同车型的策略
class GreatWallChassis : public ChassisStrategy { ... };  // CAN 协议
class SmartChassis : public ChassisStrategy { ... };      // FlexRay 协议

// 上下文类
class ChassisController {
    std::unique_ptr<ChassisStrategy> strategy_;
public:
    void setStrategy(std::unique_ptr<ChassisStrategy> s) { strategy_ = std::move(s); }
    void execute(const ControlCmd& cmd) { strategy_->sendControl(cmd); }
};
```

**你的项目：** HIL 底盘仿真模块，不同车型 CAN/FlexRay 协议不同，用策略模式各写一套实现，运行时根据车型配置切换。新车型接入只需新增一个策略类，不改框架代码。

**面试时这句话很加分：** "策略模式最适合 SDK 的多平台适配——把'会变的部分'封装为策略，接口保持不变。"

### 观察者模式（Observer）

**用途：** 一对多通知，一个对象状态变化时自动通知所有依赖者。

```cpp
class TelemetryListener {
public:
    virtual void onPosition(double lat, double lon, double alt) = 0;
    virtual void onAttitude(double roll, double pitch, double yaw) = 0;
    virtual ~TelemetryListener() = default;
};

class DroneSDK {
    std::vector<TelemetryListener*> listeners_;
public:
    void subscribe(TelemetryListener* l) { listeners_.push_back(l); }
    void notifyPosition(double lat, double lon, double alt) {
        for (auto* l : listeners_) l->onPosition(lat, lon, alt);
    }
};
```

**SDK 中的应用：** 遥测数据订阅推送——飞控状态变化时，SDK 自动回调所有注册的监听器。用户不需要轮询，SDK 推送。

### 适配器模式（Adapter）

**用途：** 把两个不兼容的接口对接起来，类似现实中的 **"转换插头"**。

```cpp
// 第三方飞控的接口（不兼容）
class DJIFlightController {
public:
    void flyToPosition(float x, float y, float z) { ... }
};

// SDK 需要的统一接口
class IFlightController {
public:
    virtual void goToWaypoint(Waypoint wp) = 0;
    virtual ~IFlightController() = default;
};

// 适配器：把 DJI 接口适配为统一接口
class DJIAdapter : public IFlightController {
    DJIFlightController& dji_;
public:
    DJIAdapter(DJIFlightController& dji) : dji_(dji) {}
    void goToWaypoint(Waypoint wp) override {
        dji_.flyToPosition(wp.x, wp.y, wp.z);  // 转换参数格式
    }
};
```

**你的项目：** Autosar RTE 层迁移到 x86——把 Autosar 的通信接口适配为 x86 平台可用的接口，上层代码不变。这就是适配器模式的实际应用。

### Pimpl 模式（Pointer to Implementation）

**用途：** **<span style="color:rgb(255, 77, 77)">隐藏实现细节，保证 ABI 兼容。改了 .cpp 实现，.h 不变</span>**，调用方不用重新编译。

```cpp
// widget.h（公开头文件）
class Widget {
public:
    Widget();
    ~Widget();
    void doSomething();
private:
    struct Impl;                    // 只声明，不暴露
    std::unique_ptr<Impl> pImpl_;   // 指针指向实现
};

// widget.cpp（实现文件，不对外暴露）
struct Widget::Impl {
    int data;
    std::string name;
    // 可以随意加成员变量，不影响 ABI
};

Widget::Widget() : pImpl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // 必须在这里定义，头文件里 Impl 是不完整类型
void Widget::doSomething() { pImpl_->data = 42; }
```

**为什么 SDK 需要 Pimpl：** <span style="color:rgb(255, 77, 77)">头文件是给用户看的，不能暴露内部实现细节</span>。Pimpl 让你随意改内部实现（加成员变量、改数据结构），<span style="color:rgb(255, 77, 77)">只要接口不变，老用户不用重新编译</span>——这就是 ABI 兼容。

### 面试话术：SDK 中设计模式的应用

> "SDK 开发中设计模式的核心价值是**抽象变化，隔离影响**。<span style="color:rgb(255, 77, 77)">工厂模式屏蔽不同机型的硬件差异，策略模式处理不同协议的数据编码，观察者模式实现遥测数据推送，适配器模式对接第三方飞控的私有协议，Pimpl 模式保证 SDK 的 ABI 兼容</span>。这些我在 HIL 框架和真值系统中都用过，思路和方法可以直接迁移到 CSDK。"

---

## 四、手撕代码 6 题

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

## 五、项目深挖话术（每个项目 3 分钟版本）

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

## 六、简历算法点防深挖（简历上写了算法词，面试官可能追问）

### 真值系统 — 多传感器时间同步

**"PTP 和 PPS 是什么？怎么做到 <1ms 的？"**

> PPS（Pulse Per Second）是 GNSS 接收器每秒发出的一个硬件脉冲信号，精度在**纳秒级**，作为系统的绝对时钟基准。PTP（Precision Time Protocol）是网络时间同步协议，域控通过 PTP 和 GNSS 主机同步系统时间。
>
> 具体做法：GNSS 输出 PPS 脉冲给激光雷达和相机做硬件触发，保证它们在同一时刻曝光/扫描。域控通过 PTP 协议把自己的系统时钟和 GNSS 对齐。最终授时精度 <1ms，用示波器测 PPS 脉冲和传感器曝光信号的时延来验证。

**"为什么需要时间同步？"**

> 多传感器融合的前提是数据对齐。比如激光雷达 10Hz、相机 30Hz、IMU 200Hz，不做时间同步的话，算法拿到的点云和图像可能差了 50ms——车速 60km/h 时 50ms 就是 0.8 米的位置偏差，感知结果直接错位。

**"同步后激光和相机的数据差多少？"**

> 硬件触发同步保证时间戳对齐在 1ms 以内。**但激光雷达一帧完整扫描本身要 100ms（10Hz），这期间的车辆运动会导致点云畸变，需要用 IMU 数据做运动补偿**。我在项目里负责时间同步，畸变补偿是感知算法团队做的。时间同步解决的是"标签对齐"，运动畸变是另一个层面的问题。

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

> 我系统学过 Transformer 架构——Self-Attention 的 QKV 计算、Multi-Head 并行、位置编码的作用。LoRA 是低秩适配，在原始权重旁加两个小矩阵 AB 做微调，只更新 AB 不动原始权重，参数量减少 90% 以上。<span style="color:rgb(255, 77, 77)"><b>DPO 是直接偏好优化，不需要训 reward model，直接用偏好数据对做对比学习</b></span>。GRPO 是分组相对策略优化，DeepSeek-R1 用的方法，用组内相对排名替代 Critic 网络。
>
> 学这些主要是为了理解大模型怎么训练和微调——虽然 CSDK 不直接写模型，但 SDK 需要支撑模型部署，了解模型结构和推理优化有助于设计更好的 API 和部署方案。

### 自主学习 — 强化学习 / MPC / VLA

**"PPO 和 MPC 有什么区别？为什么都学？"**

> PPO 是数据驱动，<span style="color:rgb(195, 117, 255)"><b>从零学习策略，不需要环境模型，但需要大量试错</b></span>。MPC 是模型驱动，<span style="color:rgb(195, 117, 255)"><b>需要精确的系统动力学模型，在线滚动优化，能处理约束</b></span>。两者互补——<span style="color:rgb(255, 77, 77)"><b>MPC 做安全约束层保证不越界，学习策略做任务级决策</b></span>。无人机上典型做法是：<span style="color:rgb(255, 77, 77)"><b>PPO/SAC 学出高层策略，底层用 MPC 或 PID 保证安全执行。</b></span>

**"为什么关注 VLA？"**

> VLA 是具身智能的核心范式，把视觉理解和动作生成统一到一个模型里。我关注它是因为 SDK 未来需要支撑这种端到端模型的部署——模型推理延迟、模型更新机制、Sim2Real 迁移，这些都对 SDK 的架构有要求。

---

## 七、算法基础（展示深度，说得越多越加分）

> 策略：SDK 岗不要求手写算法，但能讲清楚原理和"为什么这么设计"，面试官会对你刮目相看。

### 卡尔曼滤波（传感器融合基础）

**核心思想：** 把多个传感器的测量值融合成一个更准确的估计值。核心是 <span style="color:rgb(255, 77, 77)"><b>"预测 → 更新"</b> </span>两步循环。

<span style="color:rgb(255, 77, 77)"><b>预测步（用运动模型推算下一时刻状态）：</b></span>

$$
\begin{aligned}
\hat{x}_k &= F \cdot \hat{x}_{k-1} + B \cdot u_k \quad \text{（状态预测）} \\
P_k &= F \cdot P_{k-1} \cdot F^T + Q \quad \text{（协方差预测，Q 是过程噪声）}
\end{aligned}
$$

<span style="color:rgb(255, 77, 77)"><b>更新步（用传感器测量值修正预测）：</b></span>

$$
\begin{aligned}
K &= P_k \cdot H^T \cdot (H \cdot P_k \cdot H^T + R)^{-1} \quad \text{（卡尔曼增益，R 是测量噪声）} \\
\hat{x}_k &= \hat{x}_k + K \cdot (z_k - H \cdot \hat{x}_k) \quad \text{（状态修正）} \\
P_k &= (I - K \cdot H) \cdot P_k \quad \text{（协方差更新）}
\end{aligned}
$$

**关键参数：**
- Q（Process Noise Covariance，<span style="color:rgb(255, 77, 77)">过程噪声协方差</span>）大 → <span style="color:rgb(255, 77, 77)"><b>预测模型不准</b></span>，更信任传感器测量
- R（Measurement Noise Covariance，<span style="color:rgb(255, 77, 77)">测量噪声协方差</span>）大 → <span style="color:rgb(255, 77, 77)"><b>传感器不准</b></span>，更信任模型预测
- <span style="color:rgb(255, 77, 77)"><b>卡尔曼增益 K 自动平衡两者</b></span>——Q 大则 K 大，R 大则 K 小

<span style="color:rgb(255, 77, 77)"><b>数学本质：两个高斯分布相乘</b></span>

<span style="color:rgb(195, 117, 255)">预测步给出一个高斯分布</span>（"根据模型，车应该在 $\hat{x}_k$ 位置，误差 $\pm P_k$"）：

$$
\text{预测分布：} \quad \mathcal{N}(\hat{x}_k, P_k)
$$

<span style="color:rgb(195, 117, 255)">测量步给出另一个高斯分布</span>（"根据 GPS，车在 $z_k$ 位置，误差 $\pm R$"）：

$$
\text{测量分布：} \quad \mathcal{N}(z_k, R)
$$

<span style="color:rgb(195, 117, 255)"><b>融合就是两个高斯分布相乘，得到一个更窄、更确定的高斯分布：</b></span>

$$
\mathcal{N}(\mu_1, \sigma_1^2) \times \mathcal{N}(\mu_2, \sigma_2^2) \propto \mathcal{N}\!\left(\frac{\sigma_2^2\mu_1 + \sigma_1^2\mu_2}{\sigma_1^2 + \sigma_2^2},\; \frac{\sigma_1^2\sigma_2^2}{\sigma_1^2 + \sigma_2^2}\right)
$$

- <span style="color:rgb(255, 77, 77)"><span style="color:rgb(255, 77, 77)"><b>新均值 = 加权平均，谁更准（方差更小）就偏向谁</b></span></span>
- <span style="color:rgb(255, 77, 77)"><b>新方差 小于 两个原始方差中的任何一个——融合后更确定</b></span>

推广到矩阵形式就是卡尔曼更新：

$$
\begin{aligned}
K &= P_k H^T (H P_k H^T + R)^{-1} \quad \text{（卡尔曼增益 = 两个协方差的比例）} \\
\hat{x}_k &= \hat{x}_k + K(z_k - H\hat{x}_k) \quad \text{（均值加权融合）} \\
P_k &= (I - KH)P_k \quad \text{（协方差缩小）}
\end{aligned}
$$

**一句话：** 卡尔曼滤波 = 两个高斯分布相乘，得到更确定的高斯分布。预测不准就多信测量，测量不准就多信预测，K 自动算比例。

**在自动驾驶里怎么用：** GPS 10Hz 低频但绝对位置准，IMU 200Hz 高频但积分会漂移。卡尔曼滤波用 IMU 做预测（短时高频），用 GPS 做修正（长时消漂移），输出 200Hz 的准确位姿。

**EKF 和 UKF：** 标准卡尔曼只能处理线性系统（$x_k = F \cdot x_{k-1}$，$F$ 是常数矩阵）。现实世界中运动方程几乎都是非线性的——比如无人机姿态涉及四元数旋转、三角函数。**EKF（扩展卡尔曼）用雅可比矩阵 $\mathbf{J}_f$ 在每个时刻对非线性函数 $f(x)$ 做一阶泰勒展开：$f(x) \approx f(\hat{x}) + \mathbf{J}_f \cdot (x - \hat{x})$，把非线性局部近似为线性。** 代价是雅可比矩阵每步都要重算，且可能发散。**UKF（无迹卡尔曼）不用雅可比，而是用一组 sigma points 直接传播非线性变换，精度更高，计算量更小。

**SDK 视角：** CSDK 需要给融合算法提供**时间戳对齐**的多传感器数据，这是融合的前提。

### 路径规划 — A* 和 RRT

**A\*（A-Star）：**

已知地图上找最短路径。维护两个集合：
- open list：待探索的节点
- closed list：已探索过的节点

每次选 open list 中 f(n) 最小的节点扩展：

$$
f(n) = g(n) + h(n)
$$

- $g(n)$：从起点到 $n$ 的实际代价
- $h(n)$：从 $n$ 到目标的启发式估计代价（必须不高估，才能保证最优解）

**为什么 h(n) 不能高估？** 如果 h(n) > 实际距离，A* 可能跳过最优路径。h(n) 是"可接受启发"（admissible heuristic）时，保证找到最优解。

**RRT（Rapidly-exploring Random Tree，快速探索随机树）：**

高维空间、未知环境下的路径规划，不需要显式建图：
1. 在空间中随机采样一个点
2. 找到树上离采样点最近的节点
3. 从最近节点向采样点方向延伸一步（步长限制）
4. 碰撞检测，通过就加入树
5. 重复直到连接到目标

**为什么无人机用 RRT？** 无人机状态空间维度高（位置 × 姿态 × 速度），A* 在六维空间的栅格展开不可行。RRT 天然适合高维、非凸空间。

**RRT 的改进：** RRT* 在 RRT 基础上重连优化，保证渐近最优（采样越多越接近最优路径）。Informed RRT* 只在当前最优路径附近采样，效率更高。

**一句话记忆：** A* 适合低维已知地图，RRT 适合高维/未知环境。

### SLAM（同时定位与建图）

**核心矛盾：** 定位需要地图，建图需要精确位姿——鸡生蛋蛋生鸡。SLAM 同时求解这两个问题。

**前端（Frontend）：**
- 视觉 SLAM：提取 ORB/SIFT 特征点，做帧间匹配（PnP、对极几何），估计相对位姿
- 激光 SLAM：ICP（Iterative Closest Point）点云匹配，最小化点到点/点到面距离
- 前端输出粗略的位姿估计，但每帧都有误差，累积下来会漂移

**后端（Backend）：**
- 图优化（Pose Graph）：把所有位姿和观测约束建模为图，节点是位姿，边是观测约束
- 用 g2o/Ceres 等优化库做全局非线性最小二乘，消除累积误差
- 回环检测（Loop Closure）：检测是否回到之前到过的地方，添加回环约束，大幅修正漂移

**视觉 SLAM 代表框架：**
- ORB-SLAM3：经典特征点法，支持单目/双目/RGB-D，三线程并行（跟踪、局部建图、回环检测）
- VINS-Mono：视觉惯性 SLAM，紧耦合 IMU + 视觉，适合无人机

**无人机/自动驾驶中的 SLAM：** 室内飞行（无 GPS）、地下车库、隧道等场景依赖 SLAM。

### PID 控制

**公式：**

$$
u(t) = K_p \cdot e(t) + K_i \cdot \!\int\! e(t)\,dt + K_d \cdot \frac{de(t)}{dt}
$$

| 项                             | 含义  | 别名                                                   |
| ----------------------------- | --- | ---------------------------------------------------- |
| $K_p \cdot e(t)$              | 比例项 | <span style="color:rgb(255, 77, 77)">现在（当前误差）</span> |
| $K_i \cdot \!\int\! e(t)\,dt$ | 积分项 | <span style="color:rgb(255, 77, 77)">过去（误差累积）</span> |
| $K_d \cdot \frac{de(t)}{dt}$  | 微分项 | <span style="color:rgb(255, 77, 77)">未来（误差趋势）</span> |

**三项的作用和调参经验：**

| 项   | 作用                                                     | 调大效果      | 过大问题         |
| --- | ------------------------------------------------------ | --------- | ------------ |
| P   | <span style="color:rgb(255, 77, 77)">快速响应误差</span>     | 响应快、稳态误差小 | 超调、振荡        |
| I   | <span style="color:rgb(255, 77, 77)">消除稳态误差（静差</span>） | 消除静差      | 积分饱和、超调、响应变慢 |
| D   | <span style="color:rgb(255, 77, 77)">预测趋势、抑制超调</span>  | 阻尼增大、减小超调 | 放大高频噪声、系统不稳定 |

**调参顺序：** <span style="color:rgb(255, 77, 77)">先 P 调到有轻微超调 → 加 D 抑制超调 → 最后加 I 消除静差</span>。<span style="color:rgb(195, 117, 255)">I 最危险，最容易导致不稳定</span>。

**积分饱和（Integral Windup）：** <span style="color:rgb(255, 77, 77)">当执行器饱和（如电机到最大转速）时，误差持续存在</span>，<span style="color:rgb(255, 77, 77)">积分项不断累积到极大值，导致系统失控</span>。解法：<span style="color:rgb(255, 77, 77)"><b>积分限幅、积分分离</b></span>（<span style="color:rgb(255, 77, 77)">误差大时不用 I</span>）、反计算抗饱和。

**在无人机里的应用：**
- 串级 PID：外环（位置 → 期望姿态）→ 内环（姿态 → 电机转速），内环频率远高于外环
- 姿态控制：期望角度 vs 当前角度偏差 → PID → 电机 PWM 指令
- 全自主飞行 = 串级 PID × 多轴（俯仰/横滚/偏航/高度/位置）

### 深度学习感知（目标检测与分割）

**2D 检测（图像）：**
- YOLO 系列：单阶段检测器，把检测建模为回归问题，直接输出框和类别。v5/v8 是工业界主流，速度快（30+ FPS），适合嵌入式部署
- 核心思路：图像分成 S×S 网格，每个格子预测 B 个边界框 + 置信度 + 类别概率，NMS 去重

**3D 检测（激光雷达点云）：**
- PointPillars：把点云离散化为柱状体（pillar），用 PointNet 提取特征，再转成 2D 伪图像用 CNN 检测。速度快，工业界常用
- CenterPoint：基于中心点的检测，先找物体中心，再回归 3D 框属性。精度高

**语义分割：** 对每个像素/点分类（道路、车辆、行人、建筑物）。2D 用 UNet/DeepLab，3D 用 RangeNet++/KPConv。

**SDK 的支撑：** 低延迟传输大块数据（点云一帧可达几十 MB），DMA 共享内存避免拷贝，时间戳精确同步。

### 强化学习

**PPO（Proximal Policy Optimization，近端策略优化）：**
- on-policy：必须用当前策略采的样本训练，用完就扔
- 核心创新：<span style="color:rgb(255, 77, 77)">用 clip 函数限制策略更新幅度</span>，防止一步更新太大导致训练崩溃
  $$
  L^{\text{clip}} = \min\!\Big(r_t(\theta) \cdot A_t,; \text{clip}(r_t(\theta),\,1-\varepsilon,\,1+\varepsilon) \cdot A_t\Big)
  $$

  $$
  r_t(\theta) = \frac{\pi_{\text{new}}(a|s)}{\pi_{\text{old}}(a|s)} \quad \text{（新旧策略的概率比）}
  $$
- 优点：稳定，调参友好；<span style="color:rgb(255, 77, 77)"><b>缺点：样本效率低</b></span>

**SAC（Soft Actor-Critic，柔性演员-评论家）：**
- <span style="color:rgb(255, 77, 77)">off-policy：数据存 replay buffer，历史数据复用</span>
- Actor-Critic 架构：<span style="color:rgb(255, 77, 77)">Actor 输出动作，Critic 估计 Q 值</span>
- **Soft** 的核心：<span style="color:rgb(255, 77, 77)">目标函数里加了熵项 </span>H(π)，<span style="color:rgb(255, 77, 77)"><b>鼓励策略保持随机性</b></span>，不贪婪收敛
  $$
  J(\pi) = \sum \mathbb{E}\!\Big[Q(s,a) + \alpha \cdot H(\pi(\cdot|s))\Big]
  $$
- <span style="color:rgb(255, 77, 77)"><b>优点：样本效率高，探索充分</b></span>；缺点：需要调 α 温度参数

**on-policy vs off-policy：**

|       | on-policy（PPO）                                         | off-policy（SAC）                                                   |
| ----- | ------------------------------------------------------ | ----------------------------------------------------------------- |
| 训练数据  | <span style="color:rgb(255, 77, 77)">必须当前策略新采的</span>  | <span style="color:rgb(255, 77, 77)">历史数据 replay buffer 复用</span> |
| 数据利用率 | 低，采完用完就扔                                               | 高                                                                 |
| 稳定性   | <span style="color:rgb(255, 77, 77)">更稳定（无分布偏移）</span> | <span style="color:rgb(255, 77, 77)">需额外技术防过估计</span>             |
| 典型场景  | 仿真（Isaac Gym 并行数千环境）                                   | 真实机器人（数据采集成本高）                                                    |

<span style="color:rgb(255, 77, 77)"><b>价值估计方法：MC vs TD vs GAE：</b></span>

**MC（蒙特卡洛）：** <span style="color:rgb(255, 77, 77)"><b>跑完整个 episode</b></span>，用实际回报累加

$$
V(s_t) \approx r_t + r_{t+1} + r_{t+2} + \dots + r_T
$$

- <span style="color:rgb(255, 77, 77)">优点：无偏 缺点：方差大，必须等到 episode 结束，不能在线更新</span>

**TD（时序差分）：** <span style="color:rgb(255, 77, 77)"><span style="color:rgb(255, 77, 77)"><b>走一步就能更新</b></span></span>

$$
V(s_t) \approx r_t + \gamma \cdot V(s_{t+1})
$$

- <span style="color:rgb(255, 77, 77)">优点：方差小，在线更新</span> 缺点：<span style="color:rgb(255, 77, 77)">有偏</span>（$V(s_{t+1})$ 本身也是估计值，不准确）

**GAE（PPO 实际用）：** MC 和 TD 的折中，<span style="color:rgb(255, 77, 77)"><b>指数加权平均不同步数的估计</b></span>：

| λ 值 | 退化为 | 特点 |
|---|---|---|
| λ=0 | TD(0) | 只看一步，方差小但有偏 |
| λ=1 | MC | 看到结束，无偏但方差大 |
| 0<λ<1 | GAE | 折中，越远的步权重越小 |

**RL 训练到部署的完整流程：** Isaac Gym/Sim 大规模并行仿真训练 → 导出 ONNX → 量化/优化 → ARM/Orin 边缘端部署。Sim2Real 用 Domain Randomization 缩小差距。

### 模仿学习（BC / DAgger）

<span style="color:rgb(255, 77, 77)"><b>Behavior Cloning（BC，行为克隆）：</b></span>
- 最简单的模仿学习：把专家演示作为监督数据，直接学习 (observation, action) 映射
- 问题：分布偏移——训练数据来自专家轨迹，测试时小误差累积，访问到训练时没见过的状态，误差指数放大
- 示例：无人机在专家演示轨迹上 BC 训练得很好，但实际飞行时偏了一点，进入新状态，策略不知道怎么办

**DAgger（Dataset Aggregation）：**
- 迭代式数据收集，专门解决 BC 的分布偏移：
  1. 用当前策略跑，收集 (observation, 专家action) 对
  2. 把新数据加入训练集，重新训练
  3. 重复，策略逐渐覆盖更多的状态分布
- 代价：需要专家在线标注，成本高

**在 VLA 训练中：** BC 是标准预训练范式——用大规模离线演示数据做 BC，再用 RL fine-tune。

### VLA（视觉-语言-动作模型）

**核心范式：** 输入图像和语言指令，直接输出机器人动作（关节角度、末端位姿）。把 VLM 的视觉-语言理解扩展为视觉-语言-动作。

**代表性工作：**
- **RT-2（Google）：** 把动作离散化为 256 个 bin，编码为文本 token，直接用语言模型生成。优势：充分利用 VLM 的语义泛化。缺点：离散化损失精度
- **OpenVLA：** 开源 7B 模型，替代 RT-2 的闭源 PaLI-X，支持 LoRA 微调
- **π0（Physical Intelligence）：** 混合架构——VLM 做语义理解，Flow Matching 动作头输出高频连续动作，精度更高
- **ACT（Action Chunked Transformers）：** 一次预测未来 N 步动作（chunk），减少推理频率，降低累积误差
- **Diffusion Policy：** 用扩散模型建模动作分布，善于处理多模态动作（如抓取可以有多种姿态），精度高但推理慢

**核心挑战：**
- 推理延迟：7B 模型 100-500ms，需要量化 + TensorRT 加速
- 数据稀缺：真实机器人数据采集成本远高于互联网数据
- Sim2Real gap：仿真训练的策略在真实环境可能失效

**SDK 的支撑：** VLA 模型需要 SDK 提供低延迟传感器数据流、模型推理引擎的集成、模型热更新机制。

### 模型部署（ONNX / TensorRT / 量化）

**ONNX（Open Neural Network Exchange）：**
- 模型中间表示格式，PyTorch/TensorFlow 训练 → 导出 ONNX → 各推理引擎加载
- 关键：算子兼容性——有些自定义算子 ONNX 不支持，需要写 plugin

**TensorRT（NVIDIA）：**
- 推理优化引擎，针对 NVIDIA GPU/DLA 做极致优化
- 核心优化：层融合（conv+bn+relu 合并）、精度校准（FP16/INT8）、kernel auto-tuning
- 推理速度提升 2-5x，但需要针对目标硬件做 build

**量化：**
- INT8 量化：权重从 FP32 降到 INT8，模型大小减 75%，推理速度提升 2-4x
- 方法：训练后量化（PTQ，直接校准）vs 量化感知训练（QAT，训练时模拟量化）
- 风险：精度损失，尤其是小模型或关键任务

**部署流程：** PyTorch 训练 → 导出 ONNX → TensorRT build → 加载 engine → 推理

---

## 八、无人机/飞控速成知识（能说 2-3 分钟即可）

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

## 九、系统设计题："设计一个无人机 SDK"

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

## 十、高频行为问题

**Q: "你最近两年主要写 Python，C++ 还熟吗？"**

> 我在禾多做了 3 年纯 C++ 开发——传感器驱动、Autosar 迁移、CAN 通信、Linux 多线程，都是底层 C++ 项目。到元戎后虽然主力语言是 Python，但 HIL 框架的架构设计方法论是通用的，我对 C++11/14/17 的核心特性都很熟悉，写代码的手感还在，需要的话可以很快捡回来。

**Q: "你做过的是测试，和 SDK 开发有什么关系？"**

> 我做的不是纯测试，是测试平台开发，本质上是做系统架构和工程化。IFC SIL 项目更是直接做 SDK——把 Autosar 算法从特定硬件上解耦，提供 x86 平台可调用的模块化接口。这和 CSDK "向下屏蔽硬件差异、向上提供统一 API" 的目标完全一致。HIL 框架的多车型适配也是用策略模式做抽象，新车型接入不改框架代码，这和 SDK 的多平台兼容性是一个问题。

**Q: "你没有无人机经验，怎么弥补？"**

> 第一，自动驾驶和无人机在底层技术上高度相通——传感器、CAN/MAVLink 通信协议、实时系统、时间同步，这些我都有实战经验。第二，我对新领域的学习速度很快，之前在禾多从传感器应用切换到 SIL 集成开发，一个月就独立负责项目了。第三，我一直在自学机器人相关的内容，包括 Isaac Lab 仿真、强化学习、Sim2Real 部署，对无人机方向的算法和工程都有基础了解。

---

## 十一、反问面试官的问题（展示你的深度）

面试官问"你有什么想问的？"时，选 2-3 个：

1. "CSDK 目前主要支持哪些机型？不同机型之间 API 的差异大吗？是怎么做兼容性管理的？"
2. "SDK 团队和飞控团队、算法团队的协作模式是什么样的？接口设计决策的流程是什么？"
3. "目前 CSDK 的性能瓶颈在哪里？是通信延迟、序列化/反序列化，还是飞控本身的响应速度？"
4. "团队目前 SDK 的规模大概是多大？用 C++ 哪个版本？构建系统用什么？"

---

## 十二、明天时间安排

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

## 十三、面试当天注意事项

1. **不会的题不要硬编**：说"这块我了解不深，但我可以讲一下我的理解"比胡说好
2. **手撕代码时边写边讲**：解释你的思路，面试官看的是思考过程不只是结果
3. **项目经历不要背稿**：听起来假，用自然的口语讲，重点突出"我做了什么"和"结果怎么样"
4. **语速不要太快**：紧张容易语速加快，有意识地放慢
5. **如果被问到 C++ 细节想不起来**：说"我印象中是这样，但不太确定，原理上应该是..."比直接说"不知道"好
6. **面试结束前确认**：问一下"您对我还有什么想了解的？"或"后续流程大概是什么样的？"