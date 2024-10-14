# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/4/19 15:52
@作者 ： 王齐涛
@文件名称： del_files_csv.py
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from common.all_paths import DATA_PATH, LOCUSTFILE_PATH


class del_files_csv:
    def __init__(self, files_path=None, csv_path=None):
        if files_path:
            self.files_path = files_path
        if csv_path:
            self.csv_path = csv_path
        else:
            self.files_path = DATA_PATH+"\\text\\"
            self.csv_path = LOCUSTFILE_PATH
        self.del_files()
        self.del_csv()

    def del_files(self):
        """删除上述方法mkdir_files() 生成的text数据"""
        files_list = os.listdir(self.files_path)
        for i in files_list:
            c_path = os.path.join(self.files_path+i)
            os.remove(c_path)
            # print("生成的text文件全部删除成功")

    def del_csv(self):
        """删除上述方法mkdir_files() 生成的csv文件名"""
        file_list = os.listdir(self.csv_path)
        for i in file_list:
            c_path = os.path.join(self.csv_path+r"\\"+i)
            if i.endswith(".csv") is True:  # endswith()方法,返回布尔值，用来判断后缀
                os.remove(c_path)
                print("生成的csv文件全部删除成功")


if __name__ == '__main__':
    de = del_files_csv()
    de.del_files()
    de.del_csv()