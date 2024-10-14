# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 11:28
@作者 ： WangQitao
@文件名称： test_GA_stress.py
'''
import sys
import os

from testcase_data.operate_csv import write_csv_data

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from urllib.parse import urlencode
import random
from locust import TaskSet, task, constant, FastHttpUser, events, LoadTestShape
from common import all_assert
from common.logger_handler import GetLogger

# Authorization = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Authorization"]
# header = {"Authorization": f"{Authorization}", "Accept": "*/*", "Content-Type": "application/json", "Connection": "Close"}
user = 0
log = GetLogger()


class RegUserStress(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        num = random.randint(0, 999999999999999)
        # log.debug(f"获取随机数：{num}")
        return num

    @task(1)
    def test_reg_user_stress(self):
        """压力测试注册AB账号"""
        try:
            self.user_index()
            email_id = self.user_index()
            # get_code = self.test_get_email()
            params = {"email": f"testab-{email_id}@qq.com", "password": "123456", "code": "456852"}
            with self.client.post(path="/userab/rest/reg"+"?" + urlencode(params), json="", name="注册AB账号", verify=False, catch_response=True) as req:
                succeed = "注册账号---成功"
                failure = "注册账号---失败"
                all_assert.all_assert_re(req, succeed, failure)
                if req.status_code == 200:  # 将数据写入到csv文件中
                    email = req.json()["data"]["email"]
                    write_csv_data("ab3", email)

        except Exception as e:
            log.error(f"代码报错：{e}。")
            raise "IndexError: list index out of range!"


class WebsiteUser(FastHttpUser):
    tasks = [RegUserStress]
    host = "http://209.126.124.140:10002"  # 国外测试服w
    # host = "http://192.168.3.39:10001"  # 国内
    # host = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Http_AB_EN"]


if __name__ == '__main__':
    import os
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    # os.system("locust -f test_GA_stress.py --headless -u 200 -r 1 -t 13600s --skip-log-setup --only-summary --csv=../report/reg_user_stress/result --html=../report/reg_user_stress/report.html")
    os.system("locust -f test_GA_stress.py --headless -u 30 -r 1 -t 3000s")
