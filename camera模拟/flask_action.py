import os
import shutil

import zipfile
import time


def download_file(file_id):
    pass


def mearge_gt_file(param):
    pass


def unzip_zip_get_data(zip_filepath):
    """
    解压zip文件，并获取其中的数据信息
    :param zip_filepath:
    :return:
    """
    # 解压zip文件到临时目录
    temp_dir = "temp_unzip"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)  # 如果临时目录已存在，则删除它
    os.makedirs(temp_dir)  # 创建临时目录
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    for root, dirs, files in os.walk(temp_dir):
        # 定位frame文件夹
        if "frame" not in dirs:
            continue
        items = []
        for frame_dir in os.listdir(os.path.join(root, "frame")):
            item = {}
            # 构造目标子文件夹的完整路径
            if os.path.isdir(os.path.join(root, frame_dir)) and os.path.exists(os.path.join(root, frame_dir + ".txt")):
                pic_num = len(os.path.join(root, frame_dir))
                item['name'] = dir
                item['pic_num'] = pic_num
                item['action_type'] = 'camera'
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                item['create_name'] = 'admin'
                items.append(item)
                print(f"子文件夹{dir}包含{pic_num}张图片")
            else:
                print(f"子文件夹{dir}不是有效的相机数据文件夹")
            print(f"有效相机数据文件夹数量：{len(items)}")

        break # 只处理第一个frame文件夹




# def upload_data(request):
#     request_data = request.get_json()
#     file_id = request_data.get('file_id')
#     file_name = download_file(file_id)
#
#     unzip_file(file_name)
#
#     return 'success'

unzip_zip_get_data('Crawl.zip')