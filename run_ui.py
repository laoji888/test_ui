from cof import HTMLTestRunner
import time, unittest, os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


currentime = time.strftime("%Y-%m-%d %H-%M-%S")  # 获取当前时间
case_path = "./case"  # 测试用例路径
file_path = './report_ui'  # 测试报告路径


def repotr_path(file_path):  # 给测试报告排序，返回路径，并控制测试报告数量
    report_path = file_path  # 测试报告路径
    lists = os.listdir(report_path)  # 返回list
    lists.sort(key=lambda a: os.path.getatime(report_path + '//' + a))  # 以时间排序
    file = os.path.join(report_path, lists[-1])  # 返回测试报告路径

    count = os.listdir(file_path)

    # 控制报告的数量
    if len(count) > 2:
        count.sort()
        ph = './report_ui/' + count[0]
        os.remove(ph)
    else:
        pass
    return file


def email(file_path, to_email):  # 以附件方式把测试报告发送给指定的人
    s_server = 'smtp.163.com'  # 定义邮箱服务
    user = 'xztlaoji@163.com'  # 用户名
    password = 'JiYaNanbc123'  # 密码(授权密码)
    #receive = 'jiyananid@163.com'  # 收件人地址，可以有多个，用“ ，”分割

    name = os.listdir('./report_ui')  # 以list的方式返回report下的报告

    msg_total = MIMEMultipart()  # 定义类型
                                # multipart类型主要有三种子类型：
                                # mixed、alternative、related  默认mixed
    msg_total['From'] = user  # 发送方邮箱
    msg_total['To'] = ','.join(to_email)  # 接受者邮箱
    msg_total['Subject'] = '测试报告'  # 邮件的标题

    # 正文模块
    msg_raw = open(file_path, "r", encoding='utf-8').read()  # 打开
    msg = MIMEText(msg_raw, 'html')
    msg_total.attach(msg)

    # 附件模块
    mfile = MIMEApplication(open(file_path, "rb").read())  # 读取测试报告内容
    mfile.add_header('Content-Disposition', 'attachment', filename=name[-1])  # 添加附件的头信息

    # 附件摸快添加到总的里面
    msg_total.attach(mfile)
    smtp = smtplib.SMTP_SSL(s_server, 465)
    smtp.login(user, password)
    smtp.sendmail(user, to_email, msg_total.as_string())
    smtp.quit()


def my_tese():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="ui*.py")
    return discover



if __name__ == "__main__":
    report_path = "./report_ui/" + "UI_" + currentime + ".html"  # 报告保存路径
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title="csms自动化测试报告",
                                           description="自动化测试报告")
    runner.run(my_tese())  # 执行测试用例
    fp.close()  # 关闭文件

    report = repotr_path(file_path)
    e = ['jiyananid@163.com']  # 多个收件人
    email(report, e)
