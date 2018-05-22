#!/usr/bin/python
#coding:utf-8
import os
import sys
import csv
import codecs
import smtplib
import urlparse
import requests
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
reload(sys)
sys.setdefaultencoding("utf-8")

result_file = 'weakpassword.csv'
curr_dir = os.path.dirname(os.path.realpath(__file__))
RESULT = curr_dir + os.sep + result_file

def sendmail(sender,password,receivers,cc_receivers,smtpServer,subject,content,result):
    sender = sender
    password = password
    receivers = receivers
    smtp_server = smtpServer
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ','.join(receivers)
    message['Cc'] = ','.join(cc_receivers)
    message['Subject'] = subject
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    att = MIMEText(open(result, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=%s' %result_file
    message.attach(att)
    server = smtplib.SMTP(smtp_server,25)
    #server.set_debuglevel(1)
    server.login(sender,password)
    server.sendmail(sender,receivers,message.as_string())
    server.quit()

def ProjectInfo(access_token, project_url):
    payload = {'access_token': access_token}
    r = requests.get(project_url, params=payload)
    return r.json()
def PasswordInfo(username, password, password_url, ipaddress, project_code):
    parsed = urlparse.urlparse(password_url)
    hostname = parsed.hostname
    parsed = parsed._replace(netloc=ipaddress)
    ip_url = parsed.geturl()
    payload = {'username': username, 'password': password, 'project_code': project_code}
    response = requests.get(ip_url, headers={'Host': hostname}, params=payload)
    return response.json()

if __name__ == '__main__':
    access_token = 'G8G8G8G8G8G8G8G8G8G8G8G8G8G8'
    username = 'G8'
    password = '123456'
    project_url = 'http://test.G8.cn/G8/api/G8-projects'
    password_url = 'http://test.G8.com/api/project/account'
    AllInfo = ProjectInfo(access_token, project_url)
    ipaddress = '11.11.11.11'

    sender = 'ops@test.cn'
    receivers = ['luge@test.cn']
    cc_receivers = ['luge@test.cn']
    passwd = '123456'
    smtpServer = 'smtp.exmail.qq.com'  #腾讯云企业邮箱
    subject = '弱密码扫描结果'
    content = '弱密码扫描表，详见附件'

    #server = smtplib.SMTP('smtp.exmail.qq.com', 25)  # SMTP协议默认端口是25
    #server.login('pms@movee.cn', '_As1234567')

    all_list = []
    for info in AllInfo['result']:
        project_list = []
        project_code = info['code']
        pwd_info = PasswordInfo(username, password, password_url, ipaddress, project_code)
        for un in pwd_info['data']:
            if un['user_name'] == 'movee' and (un['password'] == 'sdp123' or un['password'] == '_sdp1808'):
                project_list.append(info['name'])
                project_list.append(un['user_name'])
                project_list.append(un['password'])
                project_list.append(info['backend_url'])
                all_list.append(project_list)
    with open(RESULT,"wb") as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(["project", "username", "password", "baseurl"])
        writer.writerows(all_list)
    sendmail(sender,passwd,receivers,cc_receivers,smtpServer,subject,content,RESULT)
