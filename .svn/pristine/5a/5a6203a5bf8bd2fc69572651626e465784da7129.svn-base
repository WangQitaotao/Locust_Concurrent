# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/31 17:41
@作者 ： 王齐涛
@文件名称： delete_folder_or_file.py 
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import json
import requests
header = {"Authorization": "c5667094c1da4909909950ce6c8a23d60fa6988a75504b478bb410bc4efbb4977c187a919ea44e0cb3a4a46b1ada9de2fc9e80734a0c4ebfa252e58933b385cf",
          "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}


# 批量删除文件夹
data = {"id": "root"}

# 获取该目录下的所有文件或文件夹
# re1 = requests.request(url="http://209.126.124.140:30020/rest/api/basic/list", method="post", json = data , headers=header)
# # print(re1.text)
# a = json.loads(re1.text)["data"]
# for i in range(len(a)):
#     b = json.loads(re1.text)["data"][i]["id"]
#     name = json.loads(re1.text)["data"][i]["name"]
#     if "txt" in name:   # 匹配name中含有“文件夹”的文件夹
#         data = {"id": f"{b}"}
#         re5 = requests.request(url="http://209.126.124.140:30020/rest/api/basic/delete", method="post", json=data, headers=header)
#         # print(re5.text)
#         print(i)


# 获取该目录下的所有文件或文件夹
re1 = requests.request(url="http://209.126.124.140:30020/rest/api/basic/list", method="post", json = data , headers=header)
# print(re1.text)
a = json.loads(re1.text)["data"]
for i in range(len(a)):
    b = json.loads(re1.text)["data"][i]["id"]
    name = json.loads(re1.text)["data"][i]["name"]
    data = {"id": f"{b}"}
    re5 = requests.request(url="http://209.126.124.140:30020/rest/api/basic/delete", method="post", json=data, headers=header)
    print(i)