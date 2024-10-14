import csv
import os
from locust import TaskSet, FastHttpUser, task, constant
from common.logger_handler import GetLogger
log = GetLogger()


class RegUserStress(TaskSet):

    wait_time = constant(1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = []  # 实例变量
        self.current_index = 0  # 实例变量
        self.load_image_paths(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image_paths.csv'))

    def load_image_paths(self, csv_file_path):
        try:
            with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
                csv_reader = csv.reader(file)
                self.image_paths = [row[0] for row in csv_reader if row]  # 过滤空行
            log.info(f"成功加载 {len(self.image_paths)} 张图片")
            if not self.image_paths:
                log.error("CSV文件为空或未能成功加载任何路径")
        except Exception as e:
            log.error(f"加载CSV文件出错：{e}")

    def get_next_image_path(self):
        if not self.image_paths:
            log.error("图片路径列表为空")
            return None
        image_path = self.image_paths[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.image_paths)  # 循环使用路径
        log.info(f"当前调用的图片路径是: {image_path}")
        return image_path

    @task(1)
    def test_reg_user_stress(self):
        """压力测试"""
        try:
            file_path = self.get_next_image_path()
            if not file_path or not os.path.exists(file_path):
                log.error(f"无效的图片路径：{file_path}")
                return

            with open(file_path, 'rb') as image_file:  # 确保文件在使用后关闭
                files = {'file': image_file}
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
                        log.error(f"请求失败：报错响应状态码 {req.status_code}，{req.text}")

        except Exception as e:
            log.error(f"代码报错：{e}")
            raise IndexError("处理图片时出错，索引超出范围！")


class WebsiteUser(FastHttpUser):
    tasks = [RegUserStress]
    host = "http://192.168.4.161:8001"


if __name__ == '__main__':
    os.system("locust -f infer_stress_csv.py")

