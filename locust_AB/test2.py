# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/6/2 16:01
@作者 ： WangQitao
@文件名称： infer_stress.py
'''
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import codecs
import os
import time
from pathlib import Path
from os import path
import csv
from faker import Faker
from common.all_paths import DATA_PATH, LOCUSTFILE_PATH, LOCUSTFILE_PATH_AB


fake = Faker(locale="zh_CN")    # 调用python的一个库来生成对应的测试数据
__txt_data = fake.texts(nb_texts=3, max_nb_chars=200, ext_word_list=None)  # 生成随机的文章，循环一次是2kb
__filename = fake.random_int()    # 随机数字，默认0~9999，可以通过设置min,max来设置
__folder_name = fake.name()     # 随机生成全名


def mkdir_files():
    """在本地M分区下生成txt文件，以随机的shal值来命名"""
    for i in range(1, 8690):   # 循环的次数，表示生成多少个文件夹
        filename = str(fake.sha1())
        filepath = f"M:\\AOMEIYUNDATA\\text\\"+filename + ".txt"  # 文件生成的路径
        print(f"已生成{i}个文件")
        with open(filepath, "w") as f:
            csv_name = write_csv(filepath)  # 将路径写入到csv文件中
            for j in range(1, 500):   # 文件中的数据，循环的越多数据就越大
                f.write(f"{__txt_data}+{i}+{j}+{filename}")
    return csv_name


def write_csv(csv_data):
    """写入文件名到CSV文件中"""
    with open(rf"M:\\AOMEIYUNDATA\\testdata_ab.csv", "a", newline="", encoding="utf-8") as csvfile:    # 这里必须要追加，不然写进csv的文件只有一个
        writer = csv.writer(csvfile)    # 基于文件对象构建 csv写入对象
        writer.writerow([csv_data])     # 写入csv文件类容
        csvfile.close()


if __name__ == '__main__':
    mkdir_files()


