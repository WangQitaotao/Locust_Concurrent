# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/9/6 10:53
@作者 ： WangQitao
@文件名称： test_1.py 
'''
import sys
import os

import requests
from testcase_data.operate_csv import read_csv
# 文件上传不需要"Content-Type": "multipart/form-data", 这个和text/plain  不然会报错
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
url = "http://92.204.40.146:8080/db/upload?size=4766"
header = {"Authorization":"amabt9933ce33a9874641b88186b14c63790aA2aGPp++5FCgovgnbQiWTuw2zkclr5Zp4/6yIYQZ4xZ0GaKSyuUncVKaBMwKcCiWjju2SoAvCoFVvOFEB+OLaSDxCo2/Oyx/jwP6BlHwZOPYKuQu/EtnvMRRYmY1BeoZanyemhE36AmMIHll7dBuMAEhcDLmumxeXRMQtFeM6p3owf+ozfGXYLDfP7QHgB0zvyIq2ukLf87l609a6NzVLy8Yvg/PWhj153pwvRhzJWy5WQN3HDUO2hyy9Mn98eSNCYReKXzcOY31rERyb/pSbu3kmAUmpq9q0lDotBco2uQWX4Wtilns8WebZ2owyXKQpaQoD6DRMhPNlIahsa5qOw=="}

files={'file':open('O:/test1.png','rb')}
re = requests.post(url=url, files=files, headers=header)
print(re.json())



# data = read_csv(r"M:\\AOMEIYUNDATA\\testdata_same_size_1MB.csv")
# for i in data:
#     print(i)



