# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 10:21
@作者 ： WangQitao
@文件名称： test_GA_concurrent.py
'''
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import json
import math

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


header = {"Content-Type": "application/json"}
user = 0
log = GetLogger()


class RegUserConcurrent(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_reg_user_concurrent(self):
        """并发测试"""
        try:
            payload = json.dumps([
                {
                    "m": "3d45d24d-7a39-3c32-bc9c-bd5248c57797",
                    "t": 1660745869,    # 获取时间戳
                    "w": "1",
                    "l": "1",
                    "n": "1",
                    "u": "test_wqt",
                    "v": "1",
                    "re": "10.0.0",
                    "s": "1",
                    "la": "1",
                    "o": "windows 11 home_wqt",
                    "c": "xxx",
                    "i": 1660745869,
                    "id": 20,
                    "r": 1660745869
                }
            ])
            self.user_index()
            with self.client.post("/api/v2/soft/collect", data=payload, headers=header, name="/api/v2/soft/collect", verify=False, catch_response=True) as req:
                succeed = "---成功"
                failure = "---失败"
                print(req.status_code)
                print(req)
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。")
            raise "IndexError: list index out of range!"


class StepShape(LoadTestShape):     # 逐步负载策略：每step_time秒增加step_load个用户，持续time_limit秒
    """
        step_time -- 步骤之间的时间
        step_load -- 用户在每一步增加数量
        spawn_rate -- 用户在每一步式每秒停止/启动数量
        time_limit -- 时间限制，以秒为单位
    """
    # 逐步负载策略每隔XX秒新增启动XX个用户
    # step_time = 2
    # step_load = 40
    # spawn_rate = 40
    # time_limit = 3600
    step_time = 1
    step_load = 5
    spawn_rate = 5
    time_limit = 5

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.time_limit:
            return None
        current_step = math.floor(run_time / self.step_time) + 1
        return current_step * self.step_load, self.spawn_rate


class WebsiteUser(FastHttpUser):
    tasks = [RegUserConcurrent]
    host = "https://a.aomeisoftware.com"


if __name__ == '__main__':
    import os
    # u+(t-u)*u=用户数（其中t>=u）
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    # os.system("locust -f test_GA_concurrent.py --headless --skip-log-setup --only-summary --csv=../report/GA_WEB_concurrent/result --html=../report/GA_WEB_concurrent/report.html")
    os.system("locust -f test_GA_concurrent.py")



