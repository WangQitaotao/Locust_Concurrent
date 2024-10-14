# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 11:28
@作者 ： WangQitao
@文件名称： test_GA_stress.py
'''
import json
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import random
from locust import TaskSet, task, constant, FastHttpUser, events, LoadTestShape
from common import all_assert
from common.logger_handler import GetLogger

# Authorization = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Authorization"]
header = {"Content-Type": "application/json"}
user = 0
log = GetLogger()

class RegUserStress(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        # num = random.randint(0, 999999999999999)
        # # log.debug(f"获取随机数：{num}")
        # return num

    @task(1)
    def test_reg_user_stress(self):
        """压力测试"""
        try:
            payload = json.dumps([
                {
                    "m": "3d45d24d-7a39-3c32-bc9c-bd5248c57797",
                    "t": f"{int(time.time())}",    # 获取时间戳
                    "w": "1",
                    "l": "1",
                    "n": "1",
                    "u": "test_wqt",
                    "v": "1",
                    "re": "10.0.0",
                    "s": "1",
                    "la": "1",
                    "o": "windows 11 test_locust_1401",
                    "c": "xxx",
                    "i": 1660745869,
                    "id": 20,
                    "r": 1660745869
                }
            ])

            with self.client.post(path="/api/v2/soft/collect", data=payload, headers=header, name="WEB端GA打点压力测试", verify=False, catch_response=True) as req:
                succeed = "----> 成功"
                failure = "----> 失败"
                # print(req.status_code)
                all_assert.all_assert_re(req, succeed, failure)

        except Exception as e:
            log.error(f"代码报错：{e}。")
            raise "IndexError: list index out of range!"


class WebsiteUser(FastHttpUser):
    tasks = [RegUserStress]
    host = "https://a.aomeisoftware.com"


if __name__ == '__main__':
    import os
    file_path = os.path.abspath(__file__)
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    # os.system("locust -f test_GA_stress.py --headless -u 200 -r 1 -t 13600s --skip-log-setup --only-summary --csv=../report/reg_user_stress/result --html=../report/reg_user_stress/report.html")
    os.system(f"locust -f {file_path} --headless -u 10 -r 1 -t 250s")    # --headless -u 1 -r 1 -t 5s
