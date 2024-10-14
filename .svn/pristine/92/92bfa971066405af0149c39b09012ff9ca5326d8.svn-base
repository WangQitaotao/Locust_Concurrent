# -*- encoding: utf-8 -*-
'''
@时间 ： 2023/6/9 10:49
@作者 ： WangQitao
@文件名称： test_AV.py
'''
from locust import User, task, between
import socket

import socket
from locust import Locust, TaskSet, events, task

class TCPTaskSet(TaskSet):
        def on_start(self):
                # 创建一个TCP连接
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(("62.141.43.230", 30192))  # 将地址和端口替换为你的TCP服务器的地址和端口

        def on_stop(self):
                # 关闭TCP连接
                self.client.close()

        @task
        def send_tcp_request(self):
                try:
                        # 发送TCP请求
                        self.client.send(b"Hello, TCP Server!")
                        response = self.client.recv(1024)
                        if response:
                                # 成功接收到响应
                                events.request_success.fire(
                                        request_type="tcp",
                                        name="send_tcp_request",
                                        response_time=0,
                                        response_length=len(response),
                                )
                        else:
                                # 未收到响应
                                events.request_failure.fire(
                                        request_type="tcp",
                                        name="send_tcp_request",
                                        response_time=0,
                                        exception="No response received",
                                )
                except Exception as e:
                        # 发生异常
                        events.request_failure.fire(
                                request_type="tcp",
                                name="send_tcp_request",
                                response_time=0,
                                exception=str(e),
                        )

class TCPUser(User):
        tasks = [TCPTaskSet]
        min_wait = 1000
        max_wait = 5000

if __name__ == '__main__':
        import os
        os.system("locust -f test_AV.py")

