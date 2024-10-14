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
    # 类变量，用于保存文件迭代器
    file_iterator = None

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")

    def get_image_files_from_folder(self, folder_path):
        """获取文件夹中的所有图片文件并返回一个迭代器"""
        try:
            # 获取文件夹下所有的图片文件（假设只使用 .jpg 和 .png 格式）
            image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
            # 确保文件夹中有图片文件
            if not image_files:
                raise ValueError("文件夹中没有图片文件。")
            return iter(image_files)  # 返回图片文件列表的迭代器
        except Exception as e:
            log.error(f"获取图片时出错: {e}")
            raise

    def on_start(self):
        """每个虚拟用户启动时调用一次"""
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了
        folder_path = r"M:\爬虫\低分辨率PNG格式"
        # 只在第一次调用时初始化文件迭代器
        if RegUserConcurrent.file_iterator is None:
            RegUserConcurrent.file_iterator = self.get_image_files_from_folder(folder_path)


    @task(1)
    def test_reg_user_concurrent(self):
        """并发测试"""
        try:
            # 每次请求时从文件迭代器中获取下一个图片文件
            try:
                file_path = next(RegUserConcurrent.file_iterator)
            except StopIteration:
                # 如果迭代器遍历完毕，则重新初始化迭代器
                folder_path = r"M:\爬虫\低分辨率PNG格式"
                RegUserConcurrent.file_iterator = self.get_image_files_from_folder(folder_path)
                file_path = next(RegUserConcurrent.file_iterator)

            log.debug(f"选择的图片路径：{file_path}")

            files = {
                'file': open(file_path, 'rb')  # 'rb'表示以二进制方式读取
            }
            data = {
                "outscale": 4,
                "face_enhance": False,
                "ext": "png",
                "upscale_then_downscale": False
            }
            with self.client.post(url="/infer/", data=data, files=files, name="压力测试-AI处理图片", verify=False, catch_response=True) as req:
                if req.status_code == 200:
                    log.debug("请求成功")
                else:
                    log.error(f"请求失败 ： {req.status_code}")

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


class WebsiteUser(FastHttpUser):
    tasks = [RegUserConcurrent]
    host = "http://192.168.4.161:8001"


if __name__ == '__main__':
    import os
    os.system("locust -f infer_concurrent.py")



