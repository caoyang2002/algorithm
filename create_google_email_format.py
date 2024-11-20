def read_words_from_file(filename):
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return [word.lower() for word in words]  # 将所有单词转换为小写

def create_google_email_format(word1, word2):
    return f"{word1}{word2}@gmail.com"

def main():
    filename = 'name.txt'
    words = read_words_from_file(filename)
    
    # 输出所有可能的单词拼接组合
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j:  # 确保不会与自身拼接
                email = create_google_email_format(words[i], words[j])
                print(email)

if __name__ == "__main__":
    main()

