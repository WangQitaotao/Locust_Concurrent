# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/28 12:27
@作者 ： 王齐涛
@文件名称： 1_test_debug.py
'''
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import requests
from common.all_paths import CONFIG_PATH
from common.read_yaml import ReadYaml


# 调用相关参数
Authorization = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Authorization"]
http = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Http_CB_EN"]
header = {"Authorization": f"{Authorization}", "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
print(header)

# 基本API

# # 列目录下的文件和文件夹
data = {"id": "ddc0d961101842c08ef9f30889fe9957"}
re1 = requests.request(url = f"{http}/rest/api/basic/list", method="post", json = data , headers=header)
print(re1.text)
print(len(json.loads(re1.text)["data"]))
# print(json.loads(re1.text)["data"][0]["id"])




# data = {"id": "root", "name": "文件夹6"}     # root是为一级目录
# re2 = requests.request(url = f"{http}/rest/api/basic/mkdir", method="post", json = data , headers=header)
#      # 创建文件夹
# print(type({"msg":"success"})) ["data"]["id"]
# a= json.loads(re2.text)["data"]["id"]
# print(a)
# print(type(a))




# 删除文件或文件夹
# if "success" in str(re2.text):
#     print(re2.text)
#     print(type(json.loads(re2.text)["data"]["id"]))
# a=json.loads(re2.text)["data"]["id"]
# data = {"id": f"{a}"}
# re5 = requests.request(url = f"{http}/rest/api/basic/delete", method="post", json=data, headers=header)
# print(re5.text)




# 重命名文件或文件夹
# data = {"id": "5415ec68252c48bcbbe90e142ed44536", "name": "文件夹一改为文件夹二"}
# re3 = requests.request(url = f"{http}/rest/api/basic/rename", method="post", json = data , headers=header)
# print(re3.text)




#$获取空间信息
# re4 = requests.request(url = f"{http}/rest/api/basic/space", method="post",headers=header)
# print(re4.text)




# 获取文件或文件夹信息
# data = {"id": "d83887d815f34750b853a46c2de4eca7"}
# re6 = requests.request(url = f"{http}/rest/api/basic/item", method="post", json=data, headers=header)
# print(re6.text)




# 大文件下载获取网址
# data = {"id": "7dd97a91a99143f3952920aeed087537"}
# re6 = requests.request(url = f"{http}/rest/api/basic/download_url", method="post", json=data, headers=header)
# print(re6.text)





# 大文件上传获取网址
# data = {
#     "id": "root",
#     "name": "ac-core-1.0.jar",
#     "sha1": "8a3520396a13b61e20f7595ae7dd8da420b29ff1",
#     "size": 69217852,
#     "state": ""
# }
# re7 = requests.request(url = f"{http}/rest/api/basic/space", method="post", json=data, headers=header)
# print(re7.text)





# 用户api，响应结果为id和token
# data = {"key": "", "param": ""}
# re8 = requests.request(url = f"{http}/rest/api/user/auth", method="post", json=data, headers=header)
# print(re8.text)

