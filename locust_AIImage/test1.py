import csv
import os

import requests

url = "http://192.168.4.161:8001/infer/"
file_path = r"D:\realesrgan-ncnn-vulkan-20220424-windows\input2.jpg"
files = {
    'file': open(file_path, 'rb')  # 'rb'表示以二进制方式读取
}
data = {
    "outscale": 4,
    "face_enhance": False,
    "ext": "png",
    "upscale_then_downscale": False
}
response = requests.post(url, files=files, data=data)
print(response.status_code)
# print(response.json())



# url1 = "http://192.168.4.161:8001/colorize/"
# file_path = r"D:\realesrgan-ncnn-vulkan-20220424-windows\input2.jpg"
#
# files = {
#     'file': open(file_path, 'rb')  # 'rb'表示以二进制方式读取
# }
# response1 = requests.post(url1, files=files)
# print(response1.status_code)



# 定义CSV文件名
# csv_file = 'image_paths.csv'
# # 获取文件夹中的所有文件路径并写入到CSV文件
# with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     # 遍历文件夹中的所有文件，并写入路径
#     for i in range(1, 2461):
#         writer.writerow([rf"M:\爬虫\低分辨率PNG格式\test{i}.png"])
#     file.close()
# print(f"所有文件路径已写入 {csv_file}")
