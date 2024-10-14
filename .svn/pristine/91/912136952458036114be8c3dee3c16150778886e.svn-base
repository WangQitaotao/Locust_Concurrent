# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/8 10:32
@作者 ： 王齐涛
@文件名称： operate_csv.py
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import codecs
import os
import time
from pathlib import Path
from faker import Faker
from os import path
import csv
from common.all_paths import DATA_PATH,LOCUSTFILE_PATH_AB,LOCUSTFILE_PATH_CB

fake = Faker(locale="zh_CN")    # 调用python的一个库来生成对应的测试数据
__txt_data = fake.texts(nb_texts=3, max_nb_chars=200, ext_word_list=None)  # 生成随机的文章，循环一次是2kb
__filename = 999 #fake.random_int()    # 随机数字，默认0~9999，可以通过设置min,max来设置
__folder_name = fake.name()     # 随机生成全名


def write_csv(csv_data):
    """写入文件名到CSV文件中"""
    with open(LOCUSTFILE_PATH_CB+f"/testdata{__filename}.csv", "a", newline="", encoding="utf-8") as csvfile:    # 这里必须要追加，不然写进csv的文件只有一个
        writer = csv.writer(csvfile)    # 基于文件对象构建 csv写入对象
        # writer.writerow(["txtName"])  # 构建表头
        writer.writerow([csv_data])     # 写入csv文件类容
        csvfile.close()
    return f"testdata{__filename}.csv"


def read_csv(filepath):
    """读csv文件，将读出的数据添加到data中，返回data"""
    data = []
    with open(filepath) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            data.append(row[0])
    return data

