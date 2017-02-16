#!/usr/bin/env python
#_*_coding:UTF-8 _*_
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
####SEND THE MAIL
sender = 'xuexiaojun@zhsoftbank.com'
receiver = '15810782275@163.com'
smtpserver = 'c2.icoremail.net'
username = 'xuexiaojun@zhsoftbank.com'
password = 'AAaa1234'
smtp = smtplib.SMTP()

def send_email(msg,file_name):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = file_name
    msgRoot['From'] = 'xuexiaojun@zhsoftbank.com'
    msgText = MIMEText('%s'% msg,'html','utf-8')
    msgRoot.attach(msgText)
    att = MIMEText(open('%s'% file_name, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"' % file_name
    msgRoot.attach(att)
    while 1:
        try:
            smtp.sendmail(sender, receiver, msgRoot.as_string())
            break
        except:
            try:
                smtp.connect(smtpserver)
                smtp.login(username, password)
            except:
                print "failed to login to smtp server"

if __name__ == "__main__":
    MSG="<html><h2>计息脚本日志:&nbsp;</h2><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;附件内容为%s日志内容.;</p></html>" % yesterday
    FILE = '/data/app/ctbatch/logs/vct.log'
    send_email(MSG,FILE)
