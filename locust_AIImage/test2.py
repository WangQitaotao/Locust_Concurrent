import os
import re
import os
import re
#
# def find_files_with_double_dots(directory):
#     # 列出目录下所有文件
#     for filename in os.listdir(directory):
#         # 查找包含 ".." 的文件名
#         if re.search(r'\.\.', filename):
#             print(f'File with "..": {filename}')
#
# # # 指定要处理的文件夹路径
# directory_path = r'M:\爬虫\低分辨率PNG格式'
# find_files_with_double_dots(directory_path)
# import os
# import re
#
# def rename_files_with_double_dots(directory):
#     # 列出目录中的所有文件
#     for filename in os.listdir(directory):
#         # 检查文件名中是否包含 ".."
#         if re.search(r'\.\.', filename):
#             # 将多个连续的点替换为一个点
#             new_name = re.sub(r'\.\.+', '.', filename)
#
#             # 获取旧文件的完整路径和新文件的完整路径
#             old_file = os.path.join(directory, filename)
#             new_file = os.path.join(directory, new_name)
#
#             # 重命名文件
#             if old_file != new_file:  # 避免同名文件
#                 os.rename(old_file, new_file)
#                 print(f'Renamed: {old_file} -> {new_file}')

# 指定要处理的文件夹路径
# directory_path = r'M:\爬虫\低分辨率PNG格式'
# rename_files_with_double_dots(directory_path)

import os


def rename_files_to_test_format(directory):
    # 列出目录中的所有文件（排除目录）
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # 对文件进行重命名
    for index, filename in enumerate(files, start=1):
        # 获取文件的扩展名
        file_extension = os.path.splitext(filename)[1]

        # 生成新的文件名，格式为 test1, test2, test3...
        new_name = f"test{index}{file_extension}"

        # 获取旧文件的完整路径和新文件的完整路径
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)

        # 重命名文件
        if old_file != new_file:  # 避免同名文件
            os.rename(old_file, new_file)
            print(f'Renamed: {old_file} -> {new_file}')


# 指定要处理的文件夹路径
directory_path = r'M:\爬虫\低分辨率PNG格式'
rename_files_to_test_format(directory_path)


