# 傲梅云 压力测试
分布式用户负载测试工具

--- 
## 框架设计
- request
- locust

---
## 目录结构
    common                  --公共包
    config                  --配置文件
    data                    --存放session
    locustfile              --代码执行文件
    logs                    --存放日志
    report                  --生成的报告
    send_email              --发送邮件
    testcase_data           --构造测试数据
    tools                   --工具类
    venv                    --虚拟环境
    pytest.ini              --pytest配置文件
    all.py                  --执行总文件
    requirements.txt        --依赖包
---

## 安装依赖

    在终端中执行以下命令
    pip install -r requirements.txt

    如果有部分插件安装失败，请到 https://pypi.org/ 下载插件包
---

## 执行文件

    在locustfile文件下执行对应的接口
---

## 所需条件
    执行的是傲梅云测试服，测试的前提是需要headers，通过相应的接口可以得到授权结果
---

## 运行原理
    Locust 的运行原理是完全基于事件运行的，因此可以在一台计算机上支持数千个并发用户。
    与许多其他基于事件的应用程序相比，它不使用回调（比如 Nodejs 就是属于回调，Locust 不使用这种的逻辑）。
    相反，它通过 gevent 使用轻量级进程。

    ①Jmeter是通过线程来作为虚拟用户
    ②Locust借助gevent库对协程的支持，以greenlet来实现对用户的模拟你。
    所以，在相同配置下，Locust能支持的并发用户数相比Jmeter，就不止提升了一个Level。