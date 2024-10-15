import random
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体
mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

def simulate_red_packet_grabbing(num_rounds, num_users, bot_groups):
    user_actions = defaultdict(list)
    for round in range(num_rounds):
        active_bots = set()
        for group in bot_groups:
            if round % len(bot_groups) == bot_groups.index(group):
                active_bots.update(group)

        for user in range(num_users):
            if user in active_bots:
                action = 1  # 抢红包
            else:
                action = random.choice([0, 1])  # 真人随机选择抢或不抢
            user_actions[user].append(action)

    return user_actions

def analyze_patterns(user_actions, num_users):
    pattern_lengths = range(2, 6)  # 尝试检测2到5长度的模式
    user_scores = defaultdict(int)

    for user, actions in user_actions.items():
        for length in pattern_lengths:
            patterns = defaultdict(int)
            for i in range(len(actions) - length + 1):
                pattern = tuple(actions[i:i+length])
                patterns[pattern] += 1

            # 计算模式的规律性得分
            max_pattern_count = max(patterns.values())
            pattern_score = max_pattern_count / (len(actions) - length + 1)
            user_scores[user] += pattern_score

    # 绘制用户得分分布图
    plt.figure(figsize=(10, 6))
    plt.bar(range(num_users), [user_scores[u] for u in range(num_users)])
    plt.xlabel('用户ID')
    plt.ylabel('规律性得分')
    plt.title('用户行为规律性得分分布')
    plt.savefig('user_pattern_scores.png')
    plt.close()

    return user_scores

# 模拟参数
num_rounds = 100
num_users = 50
bot_groups = [
    set(range(0, 5)),      # 机器人组 A
    set(range(5, 10)),     # 机器人组 B
    set(range(10, 15))     # 机器人组 C
]

# 运行模拟
user_actions = simulate_red_packet_grabbing(num_rounds, num_users, bot_groups)

# 分析模式
user_scores = analyze_patterns(user_actions, num_users)

# 输出可能的机器人
threshold = 1.5  # 这个阈值可以根据实际情况调整
potential_bots = [user for user, score in user_scores.items() if score > threshold]
print(f"可能的机器人用户: {potential_bots}")

# 打印确认中文显示
print("如果你能看到这行中文，说明中文显示正常。")
