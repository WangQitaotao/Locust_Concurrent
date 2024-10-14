# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 14:39
@作者 ： WangQitao
@文件名称： test_a_strategy.py
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import math
from locust import LoadTestShape

"""
用户数和每秒请求数是两个概念
要想计算服务器的每秒请求数，要通过调试，知道实际服务器处理的能力，然后再 每秒请求次数*时间=请求的总次数

"""


class CustomShape(LoadTestShape):
    """
    时间峰值策略：基于时间的峰值，每秒生成spawn_rate个用户，持续时间为time_limit
    """
    spawn_rate = 10     # 设置产生率，每秒启动/停止用户数
    time_limit = 100    # 设置时限，压测持续时长，单位秒

    def tick(self):
        """
            设置 tick()函数
            并在tick()里面调用 get_run_time()方法
            返回一个元组，包含两值：
            user_count -- 总用户数
            spawn_rate -- 每秒启动/停止用户数
            返回None时，停止负载测试
        """
        # 调用get_run_time()方法,获取压测执行的时间
        run_time = self.get_run_time()
        # 运行时长在压测最大时长内，则继续执
        if run_time < self.time_limit:
            uesr_count = round(run_time, -2)
            # 返回user_count,spawn_rate这两个参数
            return (uesr_count, self.spawn_rate)
        return None


class MyCustomShape(LoadTestShape):
    """
    时间阶段负载策略：在不同的阶段，具有不同的用户数和产生率的图形形状

    比如下面参数stages表示前10s和10-30s用户数为10；30-60s用户数为30；60-200s用户数为60；200s后用户数为120
    其中：
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
                tick_data = (stage['users'], stage['spawn_rate'])
                return tick_data
        return None


class StepShape(LoadTestShape):
    """
    逐步负载策略：每step_time秒增加step_load个用户，持续time_limit秒
        step_time -- 步骤之间的时间
        step_load -- 用户在每一步增加数量
        spawn_rate -- 用户在每一步式每秒停止/启动数量
        time_limit -- 时间限制，以秒为单位
    """
    # 逐步负载策略每隔30秒新增启动10个用户
    step_time = 30
    step_load = 10
    spawn_rate = 10
    time_limit = 600

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.time_limit:
            return None
        current_step = math.floor(run_time / self.step_time) + 1
        return current_step * self.step_load, self.spawn_rate


class DoubleWave(LoadTestShape):
    """
    自定义一个双波形图形，
    模拟在某两个时间点的最高值

    参数解析:
        min_users ： 最小用户数
        peak_one_users ： 用户在第一个峰值
        peak_two_users ： 用户在第二个峰值
        time_limit ： 测试执行总时间
    """
    min_users = 20      # 最小用户数
    peak_one_users = 60     # 第一个峰值的用户数
    peak_two_users = 40     # 第二个峰值的用户数
    time_limit = 600        # 测试执行时间

    def tick(self):
        # 将get_run_time 四舍五入
        run_time = round(self.get_run_time())
        if run_time < self.time_limit:
            user_count = (
                    (self.peak_one_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                    + (self.peak_two_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                    + self.min_users
            )
            return (round(user_count),round(user_count))
        else:
            return None