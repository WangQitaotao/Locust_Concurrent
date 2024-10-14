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