# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/6/1 20:36
@作者 ： WangQitao
@文件名称： test_upload_file_cache.py 
'''
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from urllib.parse import urlencode
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


Authorization = "amabtc87563d376274336ad57c086d1ba11beLXm9Ksz2l3vDYHuUCavrTEz4cefrWFIFvqo7Op+B5N4VvSCjQsHt+eR/G5/Ny8P9d2k6Ervsu3ko109qwSyoveLILhjpraELYRIWb12gM57ubCsH+Rqjt46/v98ykdU0OlddTcVs3Lh/bBObBKBaQGNDXKMCk529SjAcpDfkzISZfPk3OLE2jiJ4X84RKOOAvdwcxUWUYeJrwd3Tthw7mM5ChluSzk9DMrM4InIRHIN/FzvPSBIHDSZyQE6GEtzDmo2HEKmW+nFm9p4MAnQ124FGPBrvkOBkONyN4hv/Rh72d92eRlUgzzxIUdG4RDX9gdVHsm9OiHj7P5nQaZKaLA=="
headers = {"Authorization": f"{Authorization}", "Content-Type": "multipart/form-data"}
user = 0
log = GetLogger()


class UploadFileCache(TaskSet):

    wait_time = constant(1)

    def user_index(self):
        global user
        user += 1
        log.debug(f"第{user}个虚拟用户开始启动!")

    def on_start(self):
        all_locusts_spawned.wait()  # 限制在所有用户准备完成前处于等待状态,表示在内部已经处理完了

    @task(1)
    def test_reg_user_concurrent(self):
        """并发测试上传文件到缓存池"""
        try:
            self.user_index()
            # email_id = self.user_index()
            params = {"size": "8580"}
            self.file_data = {"file": open("O:/test6.png", "rb")}
            with self.client.post(path="/db/upload"+"?" + urlencode(params), files=self.file_data, name="上传文件到缓存池", verify=False, header=headers, catch_response=True) as req:
                succeed = "上传文件到缓存池---成功"
                failure = "上传文件到缓存池---失败"
                all_assert.all_assert_re(req, succeed, failure)
        except Exception as e:
            log.error(f"代码报错：{e}。")
            raise "IndexError: list index out of range!"

class WebsiteUser(FastHttpUser):
    tasks = [UploadFileCache]
    host = "http://184.168.64.56:8080"  # 国外测试服


if __name__ == '__main__':
    import os
    # u+(t-u)*u=用户数（其中t>=u）
    # os.system("locust -f test_check_file_folder.py --headless -u 100 -r 10 -t 15s -L DEBUG --logfile ../logs/locust.log")
    # os.system("locust -f test_check_file_folder.py --headless -u 10 -r 2 -t 10s --skip-log-setup")
    os.system("locust -f test_upload_file_jemter.py --headless -u 1 -r 1 -t 5s --skip-log-setup --only-summary --csv=../report/reg_user_concurrent/result --html=../report/reg_user_concurrent/report.html")
