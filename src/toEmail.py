#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class toEmail:

    sender = ''
    user = []
    sender_pass = ''
    sendFlag = False

    def __init__(self, sender, password, userlist):
        self.sender = sender
        self.sender_pass = password
        self.user = userlist
        print('init')

    def addimgfile(self, src, imgid):               # 添加图片函数，参数1:图片路径，参数2:图片ID
        print("准备打开文件 %s" % src)
        fp = open(src, 'rb')                        # 打开文件
        print(fp)
        print("打开完毕")
        msgImage = MIMEImage(fp.read())             # 创建MIMEImage对象，读取图片内容并作为参数
        fp.close()  # 关闭文件
        print("关闭完毕")
        msgImage.add_header('Content-ID', imgid)    # 指定图片文件的Content-ID,<img>标签src用到
        print("转换完毕")
        return msgImage  # 返回msgImage对象

    def sendEmail(self, path):
        print('send')
        try:
            msg = MIMEMultipart('related')          # 创建MIMEMultipart对象，采用related定义内嵌资源的邮件体

            count = 1
            for file in os.listdir(path):
                if os.path.isdir(file):
                    continue
                else:
                    filename = os.path.join(path, file)                     # 文件绝对路径
                    print(filename)
                    tmp = toEmail.addimgfile(self, filename, str(count))    # 添加图片
                    msg.attach(tmp)
                    print("读取完毕")
                    count += 1

            strtmp = ''
            for i in range(1, count):                                       # 拼接 邮件html 显示
                strtmp += """<tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
                             <td><img src="cid:%d"></td><td>
                             </tr>""" % i

            strhtml = """<table width="600" border="0" cellspacing="0" cellspacing="4">
                         <tr bgcolor="#CECFAD" height="20" style="font-size:14px">
                         <td colspan=2>以下是捕捉图</td>
                         </tr>%s</table>""" % strtmp

            msgtext = MIMEText(strhtml, "html", "utf-8")  # <img>标签的src属性是通过Content-ID来引用的

            msg.attach(msgtext)  # MIMEMultipart对象附加MIMEText的内容

            # msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
            msg['From'] = formataddr(["报警邮件", self.sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            # msg['To'] = formataddr(["FK", "监控管理员"])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "邮件测试"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
            server.login(self.sender, self.sender_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.sender, self.user, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            self.sendFlag = True
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print("发送邮件发生异常！！")


    def getFlag(self):
        return self.sendFlag


my_sender = 'xxxx'  # 发件人邮箱账号
my_pass = 'xxx'  # 发件人邮箱密码
my_user = 'jxxchao@qq.com'  # 收件人邮箱账号

# 类测试
if __name__ == '__main__':
    toE = toEmail(my_sender, my_pass, [my_user, ])
    toE.sendEmail("../image")
    print(toE.getFlag())