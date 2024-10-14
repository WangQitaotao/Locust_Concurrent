# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 10:21
@作者 ： WangQitao
@文件名称： test_GA_concurrent.py
'''
import math
import sys
import os
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



header = {"Authorization": "8b0a254d59034618994193138d92709fe3fc94aeb37140098e92be6f55ae4496df73b981ed0b42cc8a355a09b045492a46b4fabe3aee4e22a89591e30eded43b"}
user = 0
log = GetLogger()


class RegUserConcurrent(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        num = random.randint(0, 999999999999999) + random.randint(0, 9999999)
        # log.debug(f"获取随机数：{num}")
        return num

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_reg_user_concurrent(self):
        """"""
        try:
            self.user_index()
            email_id = self.user_index()
            params = {
                "id": "7c693cc1db0e4855ac1cac4549d905b3",
                "sha1": "b81d8456406c977f0d6e95a9a09e8ae2670f2f91",
                "name": f"{email_id}.png",
                "size": 70360
            }
            with self.client.post(path="/rest/api/basic/direct_upload_url", json=params, headers=header, name="AB单用户上传多文件", verify=False, catch_response=True) as req:
                succeed = "上传文件---成功"
                failure = "上传文件---失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。")
            raise "IndexError: list index out of range!"


class StepShape(LoadTestShape):
    """
    逐步负载策略：每step_time秒增加step_load个用户，持续time_limit秒
        step_time -- 步骤之间的时间
        step_load -- 用户在每一步增加数量
        spawn_rate -- 用户在每一步式每秒停止/启动数量
        time_limit -- 时间限制，以秒为单位
    """
    # 逐步负载策略每隔30秒新增启动10个用户
    step_time = 300
    step_load = 10
    spawn_rate = 50
    time_limit = 7200

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.time_limit:
            return None
        current_step = math.floor(run_time / self.step_time) + 1
        return current_step * self.step_load, self.spawn_rate


class WebsiteUser(FastHttpUser):
    tasks = [RegUserConcurrent]
    host = "https://cloud.cbackup.com"


if __name__ == '__main__':
    import os
    # u+(t-u)*u=用户数（其中t>=u）
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    # os.system("locust -f test_upload_files_concurrent_1000w.py --headless -u 500 -r 1 -t 3600s --skip-log-setup --only-summary --csv=../report/upload_1000w/result --html=../report/upload_1000w/report.html")
    os.system("locust -f test_upload_files_concurrent_1000w.py --skip-log-setup --only-summary --csv=../report/upload_1000w/result --html=../report/upload_1000w/report.html")



