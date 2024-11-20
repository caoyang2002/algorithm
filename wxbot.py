import random
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import logging
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# 设置中文字体和日志
mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_bot_behavior(num_rounds, behavior_type):
    if behavior_type == "periodic":
        return [1 if i % 3 == 0 else 0 for i in range(num_rounds)]
    elif behavior_type == "burst":
        return [1 if 20 <= i % 50 < 30 else 0 for i in range(num_rounds)]
    elif behavior_type == "random_high":
        return [1 if random.random() > 0.3 else 0 for _ in range(num_rounds)]
    elif behavior_type == "adaptive":
        behavior = []
        state = 0
        for _ in range(num_rounds):
            if random.random() < 0.1:
                state = 1 - state
            behavior.append(state)
        return behavior
    else:
        return [random.choice([0, 1]) for _ in range(num_rounds)]

def simulate_red_packet_grabbing(num_rounds, num_users, bot_configs):
    user_actions = defaultdict(list)
    logging.info(f"开始模拟 {num_rounds} 轮红包抢夺，共 {num_users} 个用户")

    for user in range(num_users):
        if user in bot_configs:
            user_actions[user] = create_bot_behavior(num_rounds, bot_configs[user])
        else:
            user_actions[user] = [random.choice([0, 1]) for _ in range(num_rounds)]

    return user_actions

def analyze_patterns(user_actions):
    pattern_lengths = range(2, 6)
    user_scores = defaultdict(int)

    for user, actions in user_actions.items():
        user_score = 0
        for length in pattern_lengths:
            patterns = defaultdict(int)
            for i in range(len(actions) - length + 1):
                pattern = tuple(actions[i:i+length])
                patterns[pattern] += 1

            max_pattern_count = max(patterns.values())
            pattern_score = max_pattern_count / (len(actions) - length + 1)
            user_score += pattern_score

        user_scores[user] = user_score

    return user_scores

def visualize_results(user_actions, user_scores, bot_configs, num_rounds, num_users):
    plt.figure(figsize=(20, 20))

    # 1. 用户行为热图
    ax1 = plt.subplot(3, 2, 1)
    actions_matrix = np.array([user_actions[u] for u in range(len(user_actions))])
    im = ax1.imshow(actions_matrix, cmap='binary', aspect='auto')
    ax1.set_title('用户行为热图', fontsize=16)
    ax1.set_xlabel('回合', fontsize=12)
    ax1.set_ylabel('用户ID', fontsize=12)
    plt.colorbar(im, label='行为 (0: 不抢, 1: 抢)')

    # 标记已知的机器人
    for bot, behavior in bot_configs.items():
        ax1.axhline(y=bot, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
        ax1.text(num_rounds, bot, behavior, fontsize=8, verticalalignment='center')

    # 2. 用户得分条形图
    ax2 = plt.subplot(3, 2, 2)
    scores = [user_scores[u] for u in range(len(user_scores))]
    bars = ax2.bar(range(len(user_scores)), scores)
    ax2.set_xlabel('用户ID', fontsize=12)
    ax2.set_ylabel('规律性得分', fontsize=12)
    ax2.set_title('用户行为规律性得分分布', fontsize=16)

    threshold = np.mean(scores) + np.std(scores)
    for i, bar in enumerate(bars):
        if i in bot_configs:
            bar.set_color('red')
        elif scores[i] > threshold:
            bar.set_color('orange')
        else:
            bar.set_color('blue')

    ax2.axhline(y=threshold, color='g', linestyle='--', label=f'检测阈值 ({threshold:.2f})')
    ax2.legend(['检测阈值', '已知机器人', '潜在机器人', '普通用户'])

    # 3. 用户行为频率分布
    ax3 = plt.subplot(3, 2, 3)
    action_freqs = [sum(user_actions[u]) / len(user_actions[u]) for u in range(num_users)]
    ax3.hist(action_freqs, bins=20, edgecolor='black')
    ax3.set_title('用户行为频率分布', fontsize=16)
    ax3.set_xlabel('抢红包频率', fontsize=12)
    ax3.set_ylabel('用户数量', fontsize=12)

    # 4. PCA 分析
    ax4 = plt.subplot(3, 2, 4)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(actions_matrix)
    scatter = ax4.scatter(pca_result[:, 0], pca_result[:, 1], c=[user_scores[u] for u in range(num_users)], cmap='viridis')
    ax4.set_title('PCA 分析结果', fontsize=16)
    ax4.set_xlabel('第一主成分', fontsize=12)
    ax4.set_ylabel('第二主成分', fontsize=12)
    plt.colorbar(scatter, label='规律性得分')

    # 5. 聚类分析
    ax5 = plt.subplot(3, 2, 5)
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_labels = kmeans.fit_predict(actions_matrix)
    ax5.scatter(pca_result[:, 0], pca_result[:, 1], c=cluster_labels, cmap='Set1')
    ax5.set_title('K-means 聚类结果', fontsize=16)
    ax5.set_xlabel('第一主成分', fontsize=12)
    ax5.set_ylabel('第二主成分', fontsize=12)

    # 6. 时间序列分析
    ax6 = plt.subplot(3, 2, 6)
    for bot, behavior in bot_configs.items():
        ax6.plot(user_actions[bot][:50], label=f'机器人 {bot} ({behavior})')
    ax6.plot(user_actions[num_users-1][:50], label='普通用户示例', color='gray')
    ax6.set_title('机器人行为时间序列 (前50轮)', fontsize=16)
    ax6.set_xlabel('回合', fontsize=12)
    ax6.set_ylabel('行为 (0: 不抢, 1: 抢)', fontsize=12)
    ax6.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig('advanced_user_behavior_analysis.png', dpi=300)
    logging.info("详细的分析结果图表已保存为 'advanced_user_behavior_analysis.png'")
    plt.close()

# 主程序
def main():
    # 模拟参数
    num_rounds = 200
    num_users = 100
    bot_configs = {
        0: "periodic",
        20: "burst",
        40: "random_high",
        60: "adaptive",
        80: "normal"
    }

    logging.info(f"模拟参数: {num_rounds} 轮, {num_users} 用户, {len(bot_configs)} 个机器人")

    try:
        # 运行模拟
        user_actions = simulate_red_packet_grabbing(num_rounds, num_users, bot_configs)

        # 分析模式
        user_scores = analyze_patterns(user_actions)

        # 可视化结果
        visualize_results(user_actions, user_scores, bot_configs, num_rounds, num_users)

        # 输出可能的机器人
        scores = list(user_scores.values())
        threshold = np.mean(scores) + np.std(scores)
        potential_bots = [user for user, score in user_scores.items() if score > threshold]
        logging.info(f"检测阈值: {threshold:.4f}")
        logging.info(f"可能的机器人用户: {potential_bots}")

        # 评估检测效果
        true_bots = set(bot_configs.keys())
        detected_bots = set(potential_bots)
        true_positives = len(true_bots & detected_bots)
        false_positives = len(detected_bots - true_bots)
        false_negatives = len(true_bots - detected_bots)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        logging.info(f"检测效果评估:")
        logging.info(f"  准确率 (Precision): {precision:.4f}")
        logging.info(f"  召回率 (Recall): {recall:.4f}")
        logging.info(f"  F1 分数: {f1_score:.4f}")

    except Exception as e:
        logging.error(f"运行过程中发生错误: {e}")

    print("脚本执行完毕，请查看日志和生成的图表文件 'advanced_user_behavior_analysis.png'。")

if __name__ == "__main__":
    main()
