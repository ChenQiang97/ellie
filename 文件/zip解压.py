import os
import shutil
from zipfile import ZipFile


def recode(raw: str) -> str:
    '''
    编码修正: 解决中文乱码问题
    '''
    try:
        return raw.encode('cp437').decode('gbk')

    except:
        return raw.encode('utf-8').decode('utf-8')


def folder_is_exists(zip_filepath, folder_to_check):
    """
    检查zip文件内是否存在某个文件夹
    :param zip_filepath:
    :param folder_to_check:
    :return:
    """
    with ZipFile(zip_filepath, 'r') as zip_ref:
        # 遍历压缩包内所有内容
        for file_or_path in zip_ref.namelist():
            # 编码修正
            file_or_path = recode(file_or_path)
            if file_or_path.endswith(folder_to_check + "/"):
                return True

    return False


def folder_is_exists_top(zip_filepath, folder_to_check):
    """
    检查zip文件内, 一级目录是否存在某个文件夹
    :param zip_filepath:
    :param folder_to_check:
    :return:
    """
    with ZipFile(zip_filepath, 'r') as zip_ref:
        # 遍历压缩包内所有内容
        for file_or_path in zip_ref.namelist():
            # 编码修正
            file_or_path = recode(file_or_path)
            if file_or_path.startswith(folder_to_check + "/"):
                return True

    return False


def zip_extract_all(zip_filepath: str, target_path: str) -> None:
    """
    解压zip压缩包到指定位置
    :param zip_filepath:
    :param target_path:
    :return:
    """
    with ZipFile(zip_filepath, 'r') as zip_ref:
        # 遍历压缩包内所有内容
        for file_or_path in zip_ref.namelist():
            # 若当前节点是文件夹
            if file_or_path.endswith('/'):
                try:
                    # 基于当前文件夹节点创建多层文件夹
                    os.makedirs(os.path.join(target_path, recode(file_or_path)))
                except FileExistsError:
                    # 若已存在则跳过创建过程
                    pass
            # 否则视作文件进行写出
            else:
                # 利用shutil.copyfileobj，从压缩包io流中提取目标文件内容写出到目标路径
                with open(os.path.join(target_path, recode(file_or_path)), 'wb') as z:
                    # 这里基于Zipfile.open()提取文件内容时需要使用原始的乱码文件名
                    shutil.copyfileobj(zip_ref.open(file_or_path), z)


# # 向已存在的指定文件夹完整解压当前读入的zip文件
# zip_extract_all(r'D:\workspace\hellolll\hellllll\hellllll.zip', '解压测试')

# print(folder_is_exists(r'D:\workspace\hellolll.zip', "新建文件夹"))

# print(folder_is_exists_top(r"D:\workspace\hellolll\hellllll\hellllll (2).zip", "test1"))

zip_extract_all(r'D:\workspace\hellolll\hellllll\hellllll (2).zip', 'act')
