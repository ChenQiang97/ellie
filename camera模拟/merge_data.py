"""
往场景中添加新数据
"""
import os
import shutil
import zipfile


def unzip_and_merge_to_folders(zip_filepath, dest_folder, is_update=False):
    """
    解压zip文件到目标文件夹，并合并到子文件夹中
    :param zip_filepath:
    :param dest_folder:
    :param is_update: 是否更新，如果为True，则删除目标文件夹中的同名文件夹，并将解压后的文件夹移动到目标文件夹中
    :return:
    """
    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    # 解压zip文件到临时目录
    temp_dir = "temp_unzip"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)  # 如果临时目录已存在，则删除它
    os.makedirs(temp_dir)  # 创建临时目录
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    for dir in os.listdir(temp_dir):
        # 构造目标子文件夹的完整路径
        if not os.path.exists(os.path.join(dest_folder, dir)):
            shutil.move(os.path.join(temp_dir, dir), dest_folder)
        else:
            if is_update:
                shutil.rmtree(os.path.join(dest_folder, dir))  # 如果目标子文件夹已存在，则删除它
                shutil.move(os.path.join(temp_dir, dir), dest_folder)  # 移动解压后的文件夹到目标文件夹
            else:
                print(f"目标子文件夹{dir}已存在，跳过")



def check_txt_and_folder(folder_path):
    # 检查txt文件和对应的文件夹是否存在
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith(".txt"):
                continue
            txt_path = os.path.join(root, file)
            dir_path = txt_path.replace(".txt", "")
            if not os.path.exists(dir_path):
                print(f"txt文件{txt_path}对应的文件夹{dir_path}不存在")
                return False
# # 使用函数
# zip_filepath = "Crawl.zip"  # 压缩文件的路径
# dest_folder = r"D:\workspace\ellie\camera模拟\data_folders\Crawl"  # 之前创建的包含子文件夹的目录
# unzip_and_merge_to_folders(zip_filepath, dest_folder)

check_txt_and_folder(r"D:\workspace\ellie\camera模拟\Crawl")