# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 10:21
@作者 ： WangQitao
@文件名称： test_GA_concurrent.py
'''
import sys
import os

import urllib3

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import json
import math

from gevent._semaphore import Semaphore
from locust import TaskSet, task, constant, FastHttpUser, events, LoadTestShape, HttpUser
from common import all_assert
from common.logger_handler import GetLogger

header = {"Content-Type": "application/json"}
log = GetLogger()


class MyUser(HttpUser):
    # 请求间隔时间
    wait_time = constant(1)
    host = 'https://a.aomeisoftware.com'

    @task
    def my_task(self):
        try:
            payload = json.dumps([
                {
                    "m": "3d45d24d-7a39-3c32-bc9c-bd5248c57797",
                    "t": 1684832226,
                    "n": "1",
                    "p": {
                        "qq": "b",
                        "ff": "C"
                    },
                    "fp": "1",
                    "w": "7",
                    "l": "1",
                    "u": "test_stress",
                    "la": "1",
                    "g": "?user=1&_utm=ok",
                    "r": "1",
                    "rd": "www.google.com",
                    "rp": "?a.html",
                    "lp": "b.html"
                }
            ])
            urllib3.disable_warnings()
            with self.client.post(url="/api/v2/soft/collect", data=payload, headers=header, name="WEB端GA打点压力测试", verify=False, catch_response=True) as req:
                succeed = "---成功"
                failure = "---失败"
                # print(req.status_code)
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。")
            raise "IndexError: list index out of range!"


class MyCustomShape(LoadTestShape):
    # 设置压测持续时长，单位秒
    time_limit = 60
    # 每秒启动/停止用户数
    spawn_rate = 10

    def tick(self):
        """
        返回一个元组，包含两值：
            user_count -- 总用户数
            spawn_rate -- 每秒启动/停止用户数
        返回None时，停止负载测试
        """
        # 获取压测执行的时间
        run_time = self.get_run_time()

        # 运行时长在压测最大时长内，则继续执行
        if run_time < self.time_limit:
            user_count = round(run_time, -1)
            return user_count, self.spawn_rate


if __name__ == '__main__':
    import os
    file_path = os.path.abspath(__file__)
    print(file_path)
    # u+(t-u)*u=用户数（其中t>=u）
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    os.system(f"locust -f {file_path}")
    # os.system("locust -f test_GA_concurrent.py --headless --skip-log-setup --only-summary --csv=../report/GA_WEB_concurrent/result --html=../report/GA_WEB_concurrent/report.html")



