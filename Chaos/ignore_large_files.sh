#!/bin/bash

# 文件大小阈值（50M，单位：字节）
SIZE_THRESHOLD=$((50 * 1024 * 1024))
# .gitignore 文件路径（当前目录）
GITIGNORE_FILE="./.gitignore"

# 初始化忽略规则数组
ignore_patterns=()

# 读取并解析 .gitignore 文件（跳过注释和空行）
if [ -f "$GITIGNORE_FILE" ]; then
    while IFS= read -r line; do
        # 跳过空行和注释行（以 # 开头）
        if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then
            continue
        fi
        # 去除行首尾空格，添加到忽略规则数组
        pattern=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
        ignore_patterns+=("$pattern")
    done < "$GITIGNORE_FILE"
fi

# 定义函数：检查文件是否匹配 .gitignore 忽略规则
is_ignored() {
    local file_path="$1"
    for pattern in "${ignore_patterns[@]}"; do
        if [[ "$file_path" == $pattern || "$file_path" == */$pattern || "$file_path" == $pattern/* ]]; then
            return 0  # 匹配到忽略规则
        fi
    done
    return 1  # 未匹配
}

# 核心逻辑：排除.git目录 + 过滤.gitignore + 去掉./前缀
find . -path ./.git -prune -o -type f -size +50M -print | while read -r file; do
    # 彻底去掉开头的 ./ 前缀
    clean_file=${file#./}
    # 检查是否被.gitignore忽略
    if ! is_ignored "$clean_file"; then
        echo "$clean_file"  # 输出无./前缀的路径
    fi
done
