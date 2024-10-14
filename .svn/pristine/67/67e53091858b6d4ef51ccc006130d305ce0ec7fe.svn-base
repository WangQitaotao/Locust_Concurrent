# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 14:29
@作者 ： WangQitao
@文件名称： 2_test_debug.py
'''
import json
import sys
import os
from urllib.parse import urlencode
import requests
from common.all_paths import CONFIG_PATH
from common.read_yaml import ReadYaml
from gevent._semaphore import Semaphore
from common.logger_handler import GetLogger
import csv
from pathlib import Path
from locust import HttpUser, TaskSet, task, SequentialTaskSet, User, FastHttpUser, task, constant, events
import base64
import hashlib
import json
from testcase_data.operate_csv import mkdir_files
from common import all_assert

# AB注册
# params = {"email": "startqq-1997154440@qq.com", "password": "wqtwan123", "code": "456852"}
# path = "http://209.126.124.140:10002/userab/rest/reg"+"?" + urlencode(params)
# # path = "http://192.168.3.39:10001/user/rest/reg"+"?" + urlencode(params)
# re1 = requests.post(url=path, data="")
# print(re1.json())
# print(re1.json()["data"]["email"])


# AB登录
# params = {"type": "web", "email": "997154440@qq.com", "password": "wqtwan123"}
# path = "http://209.126.124.140:10001/user/rest/login"+"?" + urlencode(params)
# re2 = requests.post(url=path, data="")
# print(re2.json()["data"]["token"])
# 获取傲梅云授权
# token = re2.json()["data"]["token"]
# params = {"Authorization": f"{token}"}
# path = "http://209.126.124.140:10001/user/rest/getCloudToken"
# re3 = requests.post(url=path, data=params)
# print(re3.json()["data"])
# AB备份文件到傲梅云-逻辑1
# 1.获取ID和名称
# Authorization = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Authorization"]
# url = "http://209.126.124.140:30020/rest/api/basic/direct_upload_id_name"
# header = {"Authorization": f"{Authorization}", "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
# re4 = requests.post(url=url, data=json.dumps({"count": 1}), headers=header)
# print(re4.json())
#
# # 2.获取上传网址
# url = "http://209.126.124.140:30020/rest/api/basic/direct_upload_url_only"
# header = {"Authorization": f"{Authorization}", "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
# re5 = requests.post(url=url, data={"": ""}, headers=header)
# print(re5.json())
# sys.setrecursionlimit(3000)

# 3.上传到缓存
# url = re5.json()["data"]["url"]
# files = {'file': open(r'F:\\ab_test\\Zugspitze.jpg', 'rb')}
# header1 = {"Authorization": f"{re5.json()['data']['token']}",
#            "X-Bz-File-Name": f"{re4.json()['data'][0]['name']}",
#            "Content-Type": "b2/x-auto",
#            "X-Bz-Content-Sha1": "do_not_verify"}
# print(url, header1)
# re6 = requests.post(url=url, files=files, headers=header1)
# print(re6.json())

# 4.直接上传
# url = "http://209.126.124.140:30020/rest/api/basic/direct_upload_dones"
# data = [
#     {
#         "contentLength": 0,
#         "contentSha1": "",
#         "fileId": "",
#         "id": "",
#         "name": "",
#         "pid": ""
#     }
# ]
# re7 = requests.post(url=url, data=data, headers=header)
# print(re7.json())


# AB备份文件到傲梅云-逻辑2-调用CB
# 1.AB登录获取token
# params = {"type": "web", "email": "stress-818064263875533@qq.com", "password": "wqtwan123"}
# path = "http://209.126.124.140:10002/userab/rest/login"+"?" + urlencode(params)
# re8 = requests.post(url=path, data="")
# print(re8.json())
# print(re8.json()["data"]["token"])
#
# # 2.调用cb接口，列出云盘包含数据
# url = "http://209.126.124.140:8080/drive/all"
# header = {"Authorization": f"{re8.json()['data']['token']}"}
# re9 = requests.post(url=url, data="", headers=header)
# print(re9.json())
# header_access_token = {"Authorization": f"{re9.json()[0]['data']['access_token']}"}
# print(re9.json()[0]['data']['access_token'])

# # 3.获取批量ID和Name
# url = "http://209.126.124.140:8080/cloud/uploadIdNames?count=1"
# re10 = requests.post(url=url, data="", headers=header_access_token)
# print(re10.json())
#
# # 4.上传网址
# url = "http://209.126.124.140:8080/cloud/uploadURL"
# re11 = requests.post(url=url, data="", headers=header_access_token)
# print(re11.json())

# 5.上传到缓存
# url = re11.json()["data"]["url"]
# # files = {'file': open(r'F:\\ab_test\\Zugspitze.jpg', 'rb')}
# fl = open(r'F:\ab_test\all_shopping.py', 'rb')
# files = {'files': ('all_shopping.py', fl, 'text/plain')} # 'application/octet-stream', {'Expires': '0'}
# header1 = {"Authorization": f"{re11.json()['data']['token']}",
#            "X-Bz-File-Name": f"{re10.json()['data'][0]['name']}",
#            "Content-Type": "b2/x-auto",
#            "X-Bz-Content-Sha1": "do_not_verify"}
# re12 = requests.post(url=url, files=files, headers=header1, verify=False)
# print(requests.Request('POST', url, headers=header1, files=files).prepare().body.decode('ascii')) #可以打印出来真实请求的 字段名 以及类型等信息，如果和抓取接口不一致，调整
# print(re12.text)
# print(re12.json())

# 6.批量上传
# url = "http://209.126.124.140:8080/cloud/uploadDonesNew"
# data = [
#     {
#         "contentLength": 0,
#         "contentSha1": "string",
#         "fileId": "string",
#         "id": "string",
#         "name": "string",
#         "pid": "string"
#     }
# ]
# re13 = requests.post(url=url, data=data, headers=header_access_token)
# print(re13.json())





# 检测傲梅云
# params = {"key": "789456123", "email": "stress-818064263875533@qq.com"}
# path = "http://209.126.124.140:10002/userab/rest/test/checkCloud?" + urlencode(params)
# re8 = requests.post(url=path, data="")


# header = {"Authorization": "60cfcaf35178405cbbcdeff604b96f8c3d117334b09b4f5a82bb085f923637c65828aa502ec1444097c50ab5e35f9a92d8b55bd4f55741ae9cfa3a06fdd4a4e1"}
#
# data = {
#     "id": "238dd006ed7c49da815f9e1fc8878a48",
#     "sha1":"b81d8456406c977f0d6e95a9a09e8ae2670f2f91",
#     "name":"BBBB3.png",
#     "size":70360
# }
#
# re10 = requests.post(url="http://209.126.106.37/rest/api/basic/direct_upload_url", data=data, headers=header)
# print(re10.json())






