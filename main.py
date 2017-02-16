#!/usr/bin/env python
#coding=utf8
import os
import xlwt
import xlrd
import MySQLdb
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
sql1 = '''SELECT @rownum:= @rownum+ 1 as '序号',um.`realName` as '会员姓名',um.`mobile` as '手机号码',case when LENGTH(um.`idCardNo`)= 15 then CASE when(substring(um.`idCardNo`, LENGTH(um.`idCardNo`), 1) %2= 1) THEN '男' WHEN(substring(um.`idCardNo`, LENGTH(um.`idCardNo`), 1) %2= 0) THEN '女' else '未知' end when LENGTH(um.`idCardNo`)= 18 then case WHEN(substring(um.`idCardNo`, LENGTH(um.`idCardNo`) -1, 1) %2= 1) THEN '男' WHEN(substring(um.`idCardNo`, LENGTH(um.`idCardNo`) -1, 1) %2= 0) THEN '女' ELSE '未知' end else '身份证长度错误,不是15位或18位:'+ um.`idCardNo` end as '性别', um.`registerTime` as '注册时间', su.`usedPoints` as '积分', mg.`cardname` as '等级', um1.`realName` as '客户经理', vo.`org_city` as '所在城市', um.`idCardNo` as '身份证号' FROM `user_main` um inner join `score_user` su inner join `member_grade_user` mgu INNER JOIN `member_grade` mg INNER join `user_main` um1 INNER JOIN `v_employee` ve INNER JOIN `v_organization` vo,(SELECT @rownum:= 0) temp WHERE um.`userId`= su.`userId` and um.`userId`= mgu.`userid` and mg.`id`= mgu.`gradeId` and um.`referee`= um1.`mobile` and um1.`userId`= ve.`user_main_id` and ve.`org_id`= vo.`org_id` and um.`idCardNo` is not null'''
sql_1 = sql1.replace('sadlar', yesterday)
excevey=xlwt.Workbook(encoding = 'utf-8')
excel_date_fmt = 'YY/M/D h:mm:mm'
style = xlwt.XFStyle()
style.num_format_str = excel_date_fmt
font = xlwt.Font()
font.name = 'SimSun'
style.font = font
#sql1zhixing
sheet=excevey.add_sheet('客户信息表-%s' % yesterday)
sheet.write(0,0,'序号')
sheet.write(0,1,'会员姓名')
sheet.write(0,2,'手机号码')
sheet.write(0,3,'性别')
sheet.write(0,4,'注册时间')
sheet.write(0,5,'积分')
sheet.write(0,6,'等级')
sheet.write(0,7,'客户经理')
sheet.write(0,8,'所在城市')
sheet.write(0,9,'身份证号')
row=1
conn = MySQLdb.connect(host = "192.168.1.1:3306", user = "test", passwd = "test", db = "test",charset='utf8')
cursor = conn.cursor()
cursor.execute(sql_1)
for a01, a02, a03, a04, a05, a06, a07, a08, a09, a10 in cursor.fetchall():
    sheet.write(row,0,a01)
    sheet.write(row,1,a02)
    sheet.write(row,2,a03)
    sheet.write(row,3,a04)
    sheet.write(row,4,a05)
    sheet.write(row,5,a06)
    sheet.write(row,6,a07)
    sheet.write(row,7,a08)
    sheet.write(row,8,a09)
    sheet.write(row,9,a10)
    row+=1
cursor.close()
#daochubaobiao
excevey.save ('客户信息-%s.xls' % yesterday)
cursor.close()
conn.close()
####SEND THE MAIL
sender = 'xuexiaojun@zhsoftbank.com'
receiver = 'zhangpeng@zhsoftbank.com'
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
    MSG="<html><h2>客户信息:&nbsp;</h2><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;附件内容为%s日报表,系统每日生成.&nbsp;</p></html>" % yesterday
    FILE1= '客户信息-%s.xls' % yesterday
    send_email(MSG,FILE1)
    os.system("rm -f /root/data/*.xls")
