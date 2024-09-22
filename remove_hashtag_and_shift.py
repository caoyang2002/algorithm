def update_array(original, case_array, delete_index):
    # 找到需要删除的 '#' 的位置
    position = case_array.index('#', delete_index)

    # 移除该位置的 '#'
    case_array.pop(position)

    # 找到需要补充的元素
    next_index = sum(1 for elem in case_array if elem != '#')  # 计算已填充的元素数量
    if next_index < len(original):
        case_array.append(original[next_index])

    return case_array

# 测试案例
original1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
case1 = [0, '#', 1, '#', 2, '#', 3, '#', 4, '#']
result1 = update_array(original1, case1, 1)
print(result1)  # 期望输出：[0, 1, '#', 2, '#', 3, '#', 4, '#', 5]

original2 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
case2 = ['#', '#', '#', 1, '#', 2, 2, '#', 3, '#']
result2 = update_array(original2, case2, 1)
print(result2)  # 期望输出：['#', '#', 1, '#', 2, 2, '#', 3, '#', 3]


original3 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
case3 = [1, 2, 2, 3, 3,'#','#', 3,'#', 4]
result3 = update_array(original3, case3, 1)
print(result3)  # 期望输出：['#', '#', 1, '#', 2, 2, '#', 3, '#', 3]
