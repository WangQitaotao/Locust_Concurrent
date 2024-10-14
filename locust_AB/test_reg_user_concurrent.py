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


Authorization = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Authorization"]
header = {"Authorization": f"{Authorization}", "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
user = 0
log = GetLogger()


class RegUserConcurrent(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        num = random.randint(0, 999999999999999)
        # log.debug(f"获取随机数：{num}")
        return num

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_reg_user_concurrent(self):
        """并发测试注册AB账号"""
        try:
            self.user_index()
            email_id = self.user_index()
            # get_code = self.test_get_email()
            params = {"email": f"concurrent{email_id}@qq.com", "password": "wqtwan123", "code": "456852"}
            with self.client.post(path="/user/rest/reg"+"?" + urlencode(params), json="", name="注册AB账号", verify=False, catch_response=True) as req:
                succeed = "注册账号---成功"
                failure = "注册账号---失败"
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
    # 逐步负载策略每隔30秒新增启动10个用户
    step_time = 30
    step_load = 20
    spawn_rate = 20
    time_limit = 28800

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.time_limit:
            return None
        current_step = math.floor(run_time / self.step_time) + 1
        return current_step * self.step_load, self.spawn_rate


class WebsiteUser(FastHttpUser):
    tasks = [RegUserConcurrent]
    host = "http://209.126.124.140:10001"  # 国外测试服
    # host = "http://192.168.3.39:10001"  # 国内
    # host = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Http_AB_EN"]


if __name__ == '__main__':
    import os
    # u+(t-u)*u=用户数（其中t>=u）
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    os.system("locust -f test_GA_concurrent.py --headless -u 10 -r 1 -t 15s --skip-log-setup --only-summary --csv=../report/reg_user_concurrent/result --html=../report/reg_user_concurrent/report.html")



