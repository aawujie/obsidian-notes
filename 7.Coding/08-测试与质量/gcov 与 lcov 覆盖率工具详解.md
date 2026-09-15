# gcov 与 lcov 覆盖率工具详解

> 用一个 hello world 例子，把 gcov / lcov 两个工具的职责、产物、和配合关系讲清楚。
> 这是 HIL 代码覆盖率链路的地基，理解了它才能看懂 `lcov.info`、`report.json`、`coverage.xml` 这些 AF 产物是怎么来的。

---

## 一、一句话定位

| 工具 | 是谁 | 干什么 | 产物 |
|---|---|---|---|
| **gcov** | GCC 编译器自带 | 采集原始数据：插桩 + 记录每行跑了几次 | `.gcno`（结构）、`.gcda`（命中） |
| **lcov** | IBM 写的第三方工具（现由 Linux Test Project 维护） | 整合：收集、合并、过滤、渲染 | `.info`（tracefile）、HTML 报告 |

- **gcov 是摄像头**：每个路口装一个，记录"过了几辆车"
- **lcov 是交通管控中心**：把全城摄像头数据汇总成一张热力图

名字由来：**LCOV = Linux Test Project GCOV Extension**。2002 年 IBM 的 Peter Oberparleiter 创建，最初给 Linux 内核测覆盖率，后来通用化。GNU/Linux 开源，GitHub：`https://github.com/linux-test-project/lcov`

---

## 二、完整的实验流程

### 第 1 步：写程序

```c
// hello.c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

// 这个函数故意不调用，看覆盖率怎么体现
int divide(int a, int b) {
    if (b == 0) {
        printf("不能除以零\n");
        return -1;
    }
    return a / b;
}

int main() {
    printf("Hello, gcov!\n");
    printf("1 + 2 = %d\n", add(1, 2));
    printf("3 * 4 = %d\n", multiply(3, 4));
    // divide 故意不调用
    return 0;
}
```

### 第 2 步：编译（插桩）

```bash
gcc --coverage -o hello hello.c
```

编译完目录里出现两个文件：

```
hello         ← 可执行程序本体
hello.gcno    ← 覆盖率"记账本"（代码结构：哪些行可执行、哪些是分支）
```

> **关键理解：`./hello` 和 `hello.gcno` 是同一次编译产出的配套文件。**
> gcc 一次性干了两件事：正常编译出可执行文件 + 同时在代码里埋计数器（桩），并把桩的位置写到 `.gcno`。
> `.gcno` 是**编译期产物**，跟可执行文件一一对应。

### 第 3 步：运行

```bash
./hello
```

输出：

```
Hello, gcov!
1 + 2 = 3
3 * 4 = 12
```

运行完又多了一个文件：

```
hello.gcda    ← 运行时命中数据（每个桩记了几次数）
```

> `.gcda` 是**运行期产物**，只有程序真正跑起来才会产生。

### 第 4 步：gcov 看逐行命中

```bash
gcov hello.c
# Lines executed:64.29% of 14
```

生成 `hello.c.gcov`（逐行命中次数，`#####` 表示没跑到）：

```
        1:    3:int add(int a, int b) {       ← 跑了 1 次
        1:    4:    return a + b;
    #####:   12:int divide(int a, int b) {    ← 没跑到
    #####:   13:    if (b == 0) {
    #####:   14:        printf("不能除以零\n");
    #####:   15:        return -1;
    #####:   17:    return a / b;
        1:   20:int main() {
```

### 第 5 步：lcov 整合成 .info

```bash
lcov --capture --directory . --output-file coverage.info --gcov-tool gcov
```

`coverage.info` 就是 lcov 的统一 tracefile 格式：

```
TN:
SF:/tmp/gcov-demo/hello.c        ← 源文件路径
FN:3,add                          ← 函数定义（行号,函数名）
FN:7,multiply
FN:12,divide
FN:20,main
FNDA:1,add                        ← 函数命中次数
FNDA:1,multiply
FNDA:0,divide                     ← divide 命中 0 次
FNDA:1,main
FNF:4                             ← 函数总数
FNH:3                             ← 函数命中数
DA:3,1                            ← 每行命中次数（行号,次数）
DA:4,1
DA:12,0                           ← 第 12 行命中 0 次
DA:13,0
...
LF:14                             ← 总行数
LH:9                              ← 命中行数
end_of_record
```

### 第 6 步：genhtml 渲染 HTML 报告

```bash
genhtml coverage.info --output-directory html_report
```

生成一套静态 HTML（`index.html` 总览 + 每个源文件一页），带颜色条、覆盖率百分比，给人看。

### 第 7 步（HIL 特有）：转成 AF 机器可读产物

HIL 链路里多了一步——把 `.info` 转成程序能直接读的 JSON/XML：

```bash
python3 lcov_to_af_artifacts.py --lcov coverage.info --output-dir af_out
```

产出 `report.json`（HTML 报告的 JSON 版）：

```json
{
  "summary": {
    "lines":     { "total": 14, "hit": 9, "coverage": 64.29 },
    "functions": { "total": 4,  "hit": 3, "coverage": 75.0 },
    "branches":  { "total": 0,  "hit": 0, "coverage": 0.0 }
  },
  "files": [{
    "path": "/tmp/gcov-demo/hello.c",
    "lines":     { "total": 14, "hit": 9, "coverage": 64.29 },
    "functions": { "total": 4,  "hit": 3, "coverage": 75.0 },
    "branches":  { "total": 0,  "hit": 0, "coverage": 0.0 },
    "line_hits": { "3":1, "4":1, "12":0, "13":0, "17":0 }
  }]
}
```

---

## 三、三个产物的关系（重点）

```
hello.gcno（编译期：桩埋在哪）
      +
hello.gcda（运行期：桩记了多少数）
      ↓  gcov 对账
  逐行命中数据
      ↓  lcov 整合
coverage.info（统一 tracefile）
```

| 文件 | 什么时候产生 | 记了什么 |
|---|---|---|
| `hello` | 编译 | 可执行程序本体 |
| `hello.gcno` | 编译 | 桩埋在哪些行（代码结构） |
| `hello.gcda` | 运行 | 每行的桩记了几次数（命中数据） |

> **gcno 和 gcda 名字一样、只有后缀不同，就是因为它们配对**——gcno 是"哪儿有桩"，gcda 是"桩的数"，合起来才有覆盖率。

---

## 四、HIL 覆盖率链路中的对应关系

```
1. 编 gcov driver 包：gcc --coverage        → 产出 .gcno
2. 车上跑完测试                             → 产出 .gcda（gcov 的活到此结束）
3. lcov capture 把 .gcno + .gcda 合成       → .info（lcov 接手）
4. lcov --remove 过滤第三方代码             → 干净的 lcov.info
5. genhtml 生成 HTML 报告                   → html/ 目录
6. lcov_to_af_artifacts.py 解析 .info       → report.json / coverage_summary.json / coverage.xml
7. 上传 webfile + 回调 AF
```

---

## 五、几个容易踩的坑

### 1. genhtml 并行 bug（`duplicate merge record`）

`genhtml -j 8` 并行处理时，同一个目录被两个 worker 同时处理，合并时撞车：

```
genhtml: ERROR: duplicate merge record perception_adas/src/hma
```

源码里是硬死 `die("duplicate merge record ...")`，没有容错，且 **`--ignore-errors` 对它无效**（它不走错误路径）。

**修法**：先 `-j 8`，失败自动 fallback `-j 1` 重试。单线程不存在竞态，100% 成功；正常情况享受并行速度，几乎不损失时间。

### 2. gcov 版本要匹配

编译时用的 gcc 版本，运行时 gcov 必须是同一版本，否则 `.gcno`/`.gcda` 格式对不上会报错（`version` / `mismatch` 类错误）。

### 3. 路径要一致

`.gcda` 记录的是编译时的源文件路径。如果编译后挪了目录、或删了源文件，gcov 会报 `unable to open ... No such file or directory`。genhtml 用 `--source-directory` + `--prefix` 来重新映射路径。

---

## 六、扩展阅读

- Linux 内核现在另有 **kcov**，专门针对内核态 + fuzzing（syzkaller 用 kcov），比 lcov 轻量
- 用户态程序基本就是 gcov + lcov 一统天下
- lcov 支持 differential coverage（差量覆盖率）、date/owner binning，见 arXiv:2008.07947

---

*笔记生成于 2026-09-15，示例代码在 `/tmp/gcov-demo/`*
