# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/6/1 14:15
@作者 ： WangQitao
@文件名称： test_login.py 
'''
import math
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import csv
import queue
from urllib.parse import urlencode
from common.all_paths import CONFIG_PATH, LOCUSTFILE_PATH_AB
from common.read_yaml import ReadYaml
from gevent._semaphore import Semaphore
from locust import TaskSet, task, constant, FastHttpUser, events, LoadTestShape
from common import all_assert
from common.logger_handler import GetLogger


all_locusts_spawned = Semaphore()   # 控制获取资源的线程数量
all_locusts_spawned.acquire()


@events.spawning_complete.add_listener
def on_hatch_complete(**kwargs):
    """
    Select_task类的钩子方法
    :param kwargs:
    :return:
    """
    all_locusts_spawned.release()


log = GetLogger()
user = 0

class TestLogin(TaskSet):
    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_check_file_folder(self):
        """登录"""
        try:
            self.user_index()
            test_data = self.parent.share_data.get()
            data = {"type": "web", "email": f"{test_data}", "password": "wqtwan123"}
            with self.client.post(path="http://209.126.124.140:10001/user/rest/login"+"?" + urlencode(data), json="", headers="", name="登录AB", verify=False, catch_response=True) as req:
                succeed = "登录成功"
                failure = "登录失败"
                all_assert.all_assert_re(req, succeed, failure)
                self.parent.share_data.put_nowait(test_data)
        except Exception as e:
            log.error(f"代码报错：{e}。可能是列表索引超出范围，列表中没有文件或文件夹了")
            exit(0)
            raise "IndexError: list index out of range!"


class StepShape(LoadTestShape):     # 逐步负载策略：每step_time秒增加step_load个用户，持续time_limit秒
    """
        step_time -- 步骤之间的时间
        step_load -- 用户在每一步增加数量
        spawn_rate -- 用户在每一步式每秒停止/启动数量
        time_limit -- 时间限制，以秒为单位
    """
    # 逐步负载策略每隔30秒新增启动10个用户
    step_time = 30
    step_load = 20
    spawn_rate = 20
    time_limit = 10800

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.time_limit:
            return None
        current_step = math.floor(run_time / self.step_time) + 1
        return current_step * self.step_load, self.spawn_rate


class WebsiteUser(FastHttpUser):
    tasks = [TestLogin]
    host = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Http_AB_EN"]
    file_path = LOCUSTFILE_PATH_AB+r"\testdataab.csv"
    share_data = queue.Queue()
    print(share_data)
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            share_data.put_nowait(row[0])



if __name__ == '__main__':
    os.system("locust -f test_login.py")