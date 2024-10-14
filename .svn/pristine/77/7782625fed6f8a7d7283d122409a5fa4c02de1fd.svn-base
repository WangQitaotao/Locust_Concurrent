# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/5/30 11:28
@作者 ： WangQitao
@文件名称： test_GA_stress.py
'''
import sys
import os

from testcase_data.operate_csv import read_csv

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from urllib.parse import urlencode
import random
from locust import TaskSet, task, constant, FastHttpUser, events, LoadTestShape
from common import all_assert
from common.logger_handler import GetLogger

header = {"Authorization":"amabt9933ce33a9874641b88186b14c63790aA2aGPp++5FCgovgnbQiWTuw2zkclr5Zp4/6yIYQZ4xZ0GaKSyuUncVKaBMwKcCiWjju2SoAvCoFVvOFEB+OLaSDxCo2/Oyx/jwP6BlHwZOPYKuQu/EtnvMRRYmY1BeoZanyemhE36AmMIHll7dBuMAEhcDLmumxeXRMQtFeM6p3owf+ozfGXYLDfP7QHgB0zvyIq2ukLf87l609a6NzVLy8Yvg/PWhj153pwvRhzJWy5WQN3HDUO2hyy9Mn98eSNCYReKXzcOY31rERyb/pSbu3kmAUmpq9q0lDotBco2uQWX4Wtilns8WebZ2owyXKQpaQoD6DRMhPNlIahsa5qOw=="}
user = 0
log = GetLogger()
data = read_csv(r"M:\\AOMEIYUNDATA\\testdata_same_size_1MB.csv")


class RegUserStress(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")
        # num = random.randint(0, 999999999999999)
        # # log.debug(f"获取随机数：{num}")
        return user

    @task(1)
    def test_reg_user_concurrent(self):
        """"""
        try:
            self.user_index()
            print(user)
            email_id = self.user_index()
            files={'file':open(f'{data[email_id]}', 'rb')}
            log.debug(data[email_id])
            with self.client.post(path="/db/upload?size=4766", files=files, headers=header, name="AB上传文件到DB数据库", verify=False, catch_response=True) as req:
                succeed = "上传文件---成功"
                failure = "上传文件---失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。")


class WebsiteUser(FastHttpUser):
    tasks = [RegUserStress]
    host = "http://92.204.40.146:8080" # 国外测试服w
    # host = "http://192.168.3.39:10001"  # 国内
    # host = ReadYaml().read_yaml(CONFIG_PATH + r"\\header")["Http_AB_EN"]


if __name__ == '__main__':
    import os
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    # os.system("locust -f test_GA_stress.py --headless -u 200 -r 1 -t 13600s --skip-log-setup --only-summary --csv=../report/reg_user_stress/result --html=../report/reg_user_stress/report.html")
    os.system("locust -f test_reg_user_stress_DB.py --headless -u 1 -r 1 -t 10s")
