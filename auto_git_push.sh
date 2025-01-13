#########################################################################
# File Name: auto_git_push.sh
# Author: simons
# mail: reggiesimons2cy@gmail.com
# Created Time: Tue Dec  3 08:44:56 2024
#########################################################################
#!/bin/bash
#!/bin/bash

# 设置远程仓库名称和分支，默认为origin和master
REMOTE_NAME=origin
BRANCH=main

# 遍历当前目录下的所有子目录
echo "开始提交和推送所有子目录的git更改..."
for dir in */ ; do
    # 进入子目录
	echo "-----------------------------"
    cd "$dir"
    # 检查当前目录是否是Git仓库
    if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo "目录 $dir 是一个Git仓库。"
        # 拉取最新更改
        git pull --rebase "$REMOTE_NAME" "$BRANCH"
        # 添加所有更改
        git add .
        # 提交更改
        git commit -m "Automatic update"
        # 推送到远程仓库
        git push "$REMOTE_NAME" "$BRANCH"
    else
        echo "目录 $dir 不是一个git仓库，跳过..."
    fi
    # 返回上一级目录
    cd ..
done

echo "所有子目录的git更改已提交和推送完成。"
