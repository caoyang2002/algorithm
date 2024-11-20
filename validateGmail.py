import smtplib
import dns.resolver
import re

# 验证邮箱格式
def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail.com$'
    return re.match(pattern, email) is not None

# 查找邮箱的MX记录
def find_mx_records(email):
    domain = email.split('@')[1]
    mx_records = dns.resolver.resolve(domain, 'MX')
    return [mx.exchange.to_text().rstrip('.') for mx in mx_records]

# 尝试与SMTP服务器对话
def check_email_with_smtp(email, mx_record):
    try:
        server = smtplib.SMTP(mx_record, 587)
        server.set_debuglevel(0)
        server.starttls()
        server.ehlo_or_helo_if_needed()
        server.mail('')
        code, message = server.rcpt(email)
        server.quit()
        return code, message
    except smtplib.SMTPException as e:
        return None, str(e)

# 主程序
if __name__ == "__main__":
    email_to_check = input("请输入要验证的Gmail邮箱地址：")
    
    if not validate_email_format(email_to_check):
        print("邮箱地址格式不正确。")
    else:
        mx_records = find_mx_records(email_to_check)
        if not mx_records:
            print("未找到MX记录。")
        else:
            for mx_record in mx_records:
                print(f"发现MX记录：{mx_record}（优先级{mx_records.index(mx_record)}）")
                code, message = check_email_with_smtp(email_to_check, mx_record)
                if code is not None:
                    if code == 550:
                        print(f"服务器响应: {message}")
                        print("邮箱地址不存在。")
                        break
                    else:
                        print(f"与{mx_record}对话成功，服务器响应代码：{code}")
                else:
                    print(f"与{mx_record}对话失败，错误信息：{message}")

