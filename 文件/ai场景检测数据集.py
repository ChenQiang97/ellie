"""
筛选条件: 场景/各级目录/上传用户/亮度范围/创建时间范围

注意: 为防止下发任务的消息体过大, 上传用户/亮度范围/创建时间范围 这三个条件仅在单场景时生效

数据选择流程:
1. 用户选择场景(可多选)/存储目录级别(可多选/可二三四级目录混选/根据场景动态获取), 下发任务时直接发送文件夹路径
    为防止出错, 可将单场景/多场景分标签页显示
2. 如果场景字段为单选, 则显示亮度范围筛选框/创建用户/创建时间范围筛选框, 否则不显示
3. 当用户填写后三个筛选条件中的任意一个, 场景选择框变灰, 禁止用户添加场景

页面显示筛选框: 所有条件都为空时, 选中数量为0
数据列表 + 消息提示 (当前已选中多少条数据), 不提供选中功能

默认不显示亮度筛选框, 当选中"舞台"场景时, 显示亮度范围筛选框

当选择的条件仅为场景/存储目录级别时, 下发任务直接发送文件夹路径

当选择的数据更为细分时, 需要下发任务时, 需要发送图片存储的相对路径, 如: 舞台/场景1/图片1.jpg
"""


import os
import shutil
import time

data_set_path = r'D:\新建文件夹'
target_dir = "舞台"

task_start_time = time.time()

def get_directories_until_stage(file_path, target_dir):
    # 将路径分割成各个部分
    parts = file_path.split(os.sep)

    # 找到 "舞台" 的位置
    stage_index = parts.index(target_dir)

    # 提取从 "舞台" 开始到文件名之前的所有目录
    directories = parts[parts.index(target_dir):-1]

    return directories


target_path = ""
for root, dirs, files in os.walk(data_set_path):
    for dir in dirs:
        if dir == target_dir:
            print(os.path.join(root, dir))
            target_path = os.path.join(root, dir)
            break

if target_path:
    for root, dirs, files in os.walk(target_path):
        for file in files:
            pic_path = os.path.join(root, file)
            pic_info = {}
            # pic_info['path'] = os.path.join(root, file)
            pic_info['pic_name'] = file
            pic_info['dir'] = {}
            for index, dir in enumerate(get_directories_until_stage(pic_path, target_dir)):
                if index == 0:
                    pic_info['action'] = dir
                pic_info['dir'][f'dir_{index + 1}'] = dir
            print(pic_info)

            pic_target_path = data_set_path
            for key, value in pic_info['dir'].items():
                pic_target_path = os.path.join(pic_target_path, value)

            pic_target_path = os.path.join(pic_target_path, pic_info['pic_name'])

            if not os.path.exists(pic_target_path):
                pic_target_dir = os.path.dirname(pic_target_path)
                if not os.path.exists(pic_target_dir):
                    os.makedirs(pic_target_dir)

                start_time = time.time()
                shutil.copy(pic_path, pic_target_path)
                end_time = time.time()
                print(f"Copy {pic_path} to {pic_target_path}, time cost: {end_time - start_time}s")
            else:
                print(f"{pic_target_path} already exists")

# if not os.path.exists(pic_target_path):
#     os.makedirs(pic_target_path)
#
# shutil.copy(pic_path, pic_target_path)

task_end_time = time.time()
print(f"Task completed in {task_end_time - task_start_time} seconds")