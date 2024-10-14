# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 10:21
@作者 ： WangQitao
@文件名称： test_GA_concurrent.py
'''
import math
import sys
import os

from testcase_data.operate_csv import read_csv

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import random
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


# "Content-type":"multipart/form-data","Content-Type": "binary",text/plain
header = {"Authorization":"amabt9933ce33a9874641b88186b14c63790aA2aGPp++5FCgovgnbQiWTuw2zkclr5Zp4/6yIYQZ4xZ0GaKSyuUncVKaBMwKcCiWjju2SoAvCoFVvOFEB+OLaSDxCo2/Oyx/jwP6BlHwZOPYKuQu/EtnvMRRYmY1BeoZanyemhE36AmMIHll7dBuMAEhcDLmumxeXRMQtFeM6p3owf+ozfGXYLDfP7QHgB0zvyIq2ukLf87l609a6NzVLy8Yvg/PWhj153pwvRhzJWy5WQN3HDUO2hyy9Mn98eSNCYReKXzcOY31rERyb/pSbu3kmAUmpq9q0lDotBco2uQWX4Wtilns8WebZ2owyXKQpaQoD6DRMhPNlIahsa5qOw=="}
user = 0
log = GetLogger()
data = read_csv(r"M:\\AOMEIYUNDATA\\testdata_same_size_1MB.csv")


class RegUserConcurrent(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        # num = random.randint(0, 999999999999999) + random.randint(0, 9999999)
        # log.debug(f"获取随机数：{num}")
        return user

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_reg_user_concurrent(self):
        """"""
        try:
            self.user_index()
            email_id = self.user_index()
            files={'file':open(f'{data[email_id]}', 'rb')}
            log.debug(data[email_id])
            with self.client.post(path="/db/upload?size=4766", files=files, headers=header, name="AB上传文件到DB数据库", verify=False, catch_response=True) as req:
                succeed = "上传文件---成功"
                failure = "上传文件---失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。")
            # raise "IndexError: list index out of range!"


# class StepShape(LoadTestShape):
#     """
#     逐步负载策略：每step_time秒增加step_load个用户，持续time_limit秒
#         step_time -- 步骤之间的时间
#         step_load -- 用户在每一步增加数量
#         spawn_rate -- 用户在每一步式每秒停止/启动数量
#         time_limit -- 时间限制，以秒为单位
#     """
#     # 逐步负载策略每隔30秒新增启动10个用户
#     step_time = 30
#     step_load = 10
#     spawn_rate = 10
#     time_limit = 7200
#
#     def tick(self):
#         run_time = self.get_run_time()
#         if run_time > self.time_limit:
#             return None
#         current_step = math.floor(run_time / self.step_time) + 1
#         return current_step * self.step_load, self.spawn_rate


class WebsiteUser(FastHttpUser):
    tasks = [RegUserConcurrent]
    host = "http://92.204.40.146:8080"


if __name__ == '__main__':
    import os
    # u+(t-u)*u=用户数（其中t>=u）
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    os.system("locust -f test_upload_files_concurrent_DB.py --headless -u 1 -r 1 -t 10s --skip-log-setup")
    # os.system("locust -f test_upload_files_concurrent_1000w.py --headless -u 500 -r 1 -t 3600s --skip-log-setup --only-summary --csv=../report/upload_1000w/result --html=../report/upload_1000w/report.html")
    # os.system("locust -f test_upload_files_concurrent_1000w.py --skip-log-setup --only-summary --csv=../report/upload_1000w/result --html=../report/upload_1000w/report.html")



