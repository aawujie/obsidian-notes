# GitLab MR 假冲突 — force-push 后缓存未刷新

**日期**: 2026-04-07
**MR**: hil_auto_test !1177
**分支**: `feat/wjc-blc-0402-on-migration` -> `feat/blc-interface-migration`
**Tags**: #gitlab #git #troubleshooting #hil

## 现象

MR 显示 cannot_be_merged（有冲突），但本地 git merge 合并完全正常，且源分支是目标分支的纯 fast-forward。

## 根因

两个分支在短时间内（3 分钟内）经历了 rebase + force-push：

| 时间 | 事件 |
|------|------|
| 14:52 | 创建目标分支（旧 rebase 历史） |
| 14:54 | Force-push 目标分支（整个 commit 链 SHA 变化） |
| 14:55 | Push 源分支（正确基于新目标） |

GitLab 在最初计算 merge status 时，两个分支基于不同的 rebase 历史：
- 同名 commit 有不同 SHA（独立 rebase 产生）
- 旧目标分支额外包含 60+ 个 master merge commit

force-push 后两个分支已正确对齐（纯 fast-forward），但 GitLab 缓存了旧的冲突判定。

## 诊断方法

1. 本地 fetch 两个分支
2. 用 git merge-base 检查是否 fast-forward（merge-base 等于 target HEAD）
3. 用 git log 检查双方独有 commit（target 独有应为空）
4. 用 git worktree 做试合并验证

## 解决方法

### 方法 1: Git 命令（推荐）

force-push 到同一个 commit，触发 GitLab push event：
- `git push origin source-branch --force-with-lease`

或 push 空 commit：
- `git commit --allow-empty -m "chore: trigger merge status refresh"`
- `git push origin source-branch`

### 方法 2: GitLab API

访问 MR 的 merge_ref 端点强制重新计算。

### 方法 3: 更新 MR 属性

通过 API PUT 更新 MR title 等任意字段，也能触发重新计算。

## 教训

- GitLab merge status 是缓存的，force-push 后可能不会立即更新
- 短时间内连续 force-push 多个分支更容易触发此问题
- 遇到 MR 显示冲突时，先本地验证再判断是否为缓存问题
- merge_ref API 端点是最可靠的刷新方式
