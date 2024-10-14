# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 10:21
@作者 ： WangQitao
@文件名称： test_GA_concurrent.py
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import json
import math
from urllib.parse import urlencode
import random
from common.all_paths import CONFIG_PATH
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


# Authorization = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Authorization"]
# header = {"Authorization": f"{Authorization}", "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
# user = 0
log = GetLogger()


class RegUserConcurrent(TaskSet):

    wait_time = constant(1)

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_reg_user_concurrent(self):
        """并发测试注册AB账号"""
        try:
            header = {"Authorization":"amabt3df1f70449434f2f8e16351877796e81bjysjUxytUYCs/lqW8wfmU+WDokOFf2nincD67OLx7tqz1iGhk0KB7q/pAKpVq2kZoopEQsBaUdIondn/MgOrBp3bNMO8fLPcyHtqAFcBMMjYLlMqG731bWJszCDyKvkSFkQvUPjIVUwJoJeJ5FuV48NqIgcjbIs3fhtB4gKDn730IkeT+y5/c4oKAEfm1JaAr3o8tyECMFi0Um4FmQxCwyCIuw+DfkTIK+Q12S67BQ4KZ5owawlYlS4IJselmwG/tJFtS48ehOL1ywXTtUQ3pS8UpDArpmCcRTSJejawkRfRn8pTSdo9Y61+s9rVxftdOKLOY7HmEdKi4hsdCxBbQ=="}
            with self.client.post(path="/task/basic?start=0&length=3", json="", name="登录AB",headers=header, verify=False, catch_response=True) as req:
                succeed = "注册账号---成功"
                failure = "注册账号---失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。")
            raise "IndexError: list index out of range!"


class WebsiteUser(FastHttpUser):
    tasks = [RegUserConcurrent]
    host = "http://184.168.64.64:8080"  # 国外测试服
    # host = "http://192.168.3.39:10001"  # 国内
    # host = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Http_AB_EN"]


if __name__ == '__main__':
    import os
    # u+(t-u)*u=用户数（其中t>=u）
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    os.system("locust -f test_reg_user_concurrent_test1111.py --headless -u 500 -r 1 -t 3600s --skip-log-setup --only-summary --csv=../report/test1/result --html=../report/test1/report.html")



