#!/usr/bin/env python
# encoding: utf-8
import urlparse
import sys
import csv
import requests
reload(sys)
sys.setdefaultencoding("utf-8")

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
    access_token = 'G8G8G8G8G8G8G8G8'
    username = 'luge'
    password = 'lugehaoshuai'
    project_url = 'http://pms.G8.cn/pms/api/get-simple-projects'
    password_url = 'http://pub.G8.com/api/project/account'
    AllInfo = ProjectInfo(access_token, project_url)
    ipaddress = '11.11.11.11'
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
    with open("weakpassword.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["project", "username", "password", "baseurl"])
        writer.writerows(all_list)

