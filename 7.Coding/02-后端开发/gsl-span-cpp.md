---
title: gsl::span 与 std::span — C++ 非拥有内存视图
type: concept
created: 2026-07-30
updated: 2026-07-30
tags: [cpp, gsl, span, memory, guidelines]
sources: []
---

# gsl::span — C++ 非拥有内存视图

## 两个 GSL 不要搞混

- **GNU Scientific Library** — 数值计算库（线性代数、积分、FFT 等）
- **Guidelines Support Library（微软）** — C++ Core Guidelines 的配套实现，`gsl::span` 来自这里

## 什么是 span

`gsl::span` 是对**连续内存的非拥有视图**，本质是 `{指针 + 长度}` 的封装。

### 核心区别：拥有权

| | 拥有数据 | 管理内存 | 可以单独存在 |
|:---|:---:|:---:|:---:|
| `std::vector` | ✅ | ✅ | ✅ |
| `gsl::span` | ❌ | ❌ | ❌（依赖原数据） |

类比：
- `vector` = 买了一本书，书是你的
- `span` = 借别人的书看，不拥有，看完还回去

## 用法

```cpp
#include <gsl/span>

void process(gsl::span<int> data) {
    for (auto& x : data) {
        x *= 2;
    }
}

// 以下全部可以传入
int arr[] = {1, 2, 3, 4, 5};
std::vector<int> vec = {1, 2, 3};
std::array<int, 5> a = {1, 2, 3, 4, 5};

process(arr);          // 原生数组
process(vec);          // vector
process(a);            // std::array
process({arr + 1, 3}); // 从中间取3个（指针 + 长度）
```

## 可以指向哪些对象

只要内存连续，都行：

- 原生数组 `int[]`
- `std::array`
- `std::vector`
- 原始指针 + 长度 `{ptr, n}`
- 某个容器的子区间

## 为什么用 span 而不是引用

```cpp
// ❌ 只能接 vector，不够通用
void f(std::vector<int>& v) { ... }

// ✅ 数组/vector/array 都能传，接口统一
void f(gsl::span<int> s) { ... }
```

## 编译期 vs 运行期大小

```cpp
gsl::span<int>     s;     // 动态大小（运行期确定）
gsl::span<int, 5>  s;     // 静态大小（编译期固定）
```

## C++20 标准化

C++20 已将 `span` 纳入标准库：

```cpp
#include <span>
std::span<int> s = vec;   // 不再需要 GSL 依赖
```
