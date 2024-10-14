# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/12/31 16:52
@作者 ： 王齐涛
@文件名称： test_check_file_folder.py    ok
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))  # 特别注意这个必须放在最前面。解决pytyhon的包引用的处理的问题，如果不要这个，调用封装函数的时候就会报错


from gevent._semaphore import Semaphore
from locust import TaskSet, task, constant, FastHttpUser, events
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


class CheckFile(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_check_file_folder(self):
        """查看列目录下的文件或文件夹"""
        try:
            self.user_index()
            data = {
                "code": "string",
                "driveCount": 0,
                "loadDetail": "true",
                "password": "123456",
                "rememberMe": "true",
                "state": "string",
                "taskCount": 0,
                "type": "string",
                "username": "a123@163.com"
            }
            with self.client.post(path="/user/login", json=data, headers=header, name="CB登录", verify=False, catch_response=True) as req:
                succeed = "登录成功"
                failure = "登录失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。可能是列表索引超出范围，列表中没有文件或文件夹了")
            raise "IndexError: list index out of range!"


class WebsiteUser(FastHttpUser):
    tasks = [CheckFile]
    host = "209.126.124.140"


if __name__ == '__main__':
    import os
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    # os.system("locust -f test_check_file_folder.py --headless -u 5 -r 1 -t 6s --skip-log-setup --only-summary --csv=../report/check_file_folder/result --html=../report/check_file_folder/report.html")
    os.system("locust -f test_cb_login.py --headless -u 1 -r 1 -t 10s --skip-log-setup")

#  --headless -u 10 -r 1 -t 11s   表示10+(11-10)*10=20个虚拟用户    u+(t-u)*u=用户数（其中t>=u）
