#########################################################################
# File Name: bit.sh
# Author: ma6174
# mail: ma6174@163.com
# Created Time: Thu Oct  3 08:15:34 2024
#########################################################################
#!/bin/bash
#!/bin/bash

str1="1000010010101101111111100000101011010001001111100001001011001011"
str2="1000010010101101011111100000101011010001001111100001101010001011"

# 获取两个字符串的长度
len1=${#str1}
len2=${#str2}
max_len=$(( len1 > len2 ? len1 : len2 ))

# ANSI 转义序列
bold=$(tput bold)
reset=$(tput sgr0)
red=$(tput setaf 1)
green=$(tput setaf 2)

# 输出字符串的基础格式
echo -e "${bold}String 1:${reset} $str1"
echo -e "${bold}String 2:${reset} $str2"
echo ""

# 遍历字符串，比较字符
for (( i=0; i<max_len; i++ )); do
  char1="${str1:i:1}"
  char2="${str2:i:1}"

  if [[ "$char1" != "$char2" ]]; then
    # 构建新的字符串，标记不同的字符
    output1="${str1:0:i}${red}${bold}${char1}${reset}${str1:i+1}"
    output2="${str2:0:i}${green}${bold}${char2}${reset}${str2:i+1}"
    echo "Position $i:"
    echo -e "String 1: $output1"
    echo -e "String 2: $output2"
    echo ""
  fi
done

