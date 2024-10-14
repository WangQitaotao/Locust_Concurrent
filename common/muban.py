import math
import os

from locust import LoadTestShape

from common.logger_handler import GetLogger


"""
模板，实例代码
"""
log = GetLogger()

os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
os.system("locust -f test_GA_stress.py --headless -u 200 -r 1 -t 13600s --skip-log-setup --only-summary --csv=../report/reg_user_stress/result --html=../report/reg_user_stress/report.html")
os.system(f"locust -f test_GA_stress.py --headless -u 10 -r 1 -t 250s")    # --headless -u 1 -r 1 -t 5s


class StepShape(LoadTestShape):     # 逐步负载策略：每step_time秒增加step_load个用户，持续time_limit秒
    """
        step_time -- 步骤之间的时间
        step_load -- 用户在每一步增加数量
        spawn_rate -- 用户在每一步式每秒停止/启动数量
        time_limit -- 时间限制，以秒为单位
    """
    step_time = 1
    step_load = 1
    spawn_rate = 1
    time_limit = 10

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.time_limit:
            return None
        current_step = math.floor(run_time / self.step_time) + 1
        log.debug(f"当前步骤：{current_step}, 用户数：{current_step * self.step_load}, 启动速率：{self.spawn_rate}")
        return current_step * self.step_load, self.spawn_rate


class MyCustomShape(LoadTestShape):     # 时间阶段负载策略
    """
        ps:在不同的阶段 具有不同的用户数和 产生率的 图形形状
        time -- 持续时间经过多少秒后，进入到下个阶段
        users -- 总用户数
        spawn_rate -- 产生率，即每秒启动/停止的用户数
    """
    stages = [
        {"time": 10, "users": 10, "spawn_rate": 10},
        {"time": 30, "users": 30, "spawn_rate": 10},
        {"time": 60, "users": 60, "spawn_rate": 10},
        {"time": 200, "users": 120, "spawn_rate": 10},
    ]
    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage['time']:
                tick_data = (stage['users'],stage['spawn_rate'])
                return tick_data
        return None


class CustomShape(LoadTestShape):   # 时间峰值策略
    # 设置时限
    time_limit = 600
    # 设置产生率
    spawn_rate = 20

    def tick(self):
        '''
        设置 tick()函数
        并在tick()里面调用 get_run_time()方法
        '''

        # 调用get_run_time()方法
        run_time = self.get_run_time()
        # 运行时间在 10分钟之内，则继续执行
        if run_time < self.time_limit:
            uesr_count = round(run_time, -2)
            # 返回user_count,spawn_rate这两个参数
            return (uesr_count, self.spawn_rate)

        return None