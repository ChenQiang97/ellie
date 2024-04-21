"""
往场景中添加新数据
"""
import os
import shutil
import zipfile


def unzip_and_merge_to_folders(zip_filepath, dest_folder):
    # 解压zip文件到目标文件夹
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
            # 此处将记录写入mongodb数据库，待完成

def check_txt_and_folder(folder_path):
    # 检查txt文件和对应的文件夹是否存在
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
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