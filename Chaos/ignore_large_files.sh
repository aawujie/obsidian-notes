# 查找大于100MB的文件，排除.git目录
find . -path ./\.git -prune -o -type f -size +100M -print
