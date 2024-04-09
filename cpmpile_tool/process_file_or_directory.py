"""
1. 将指定目录下的py文件, 编译为pyc  单个文件/目录
2. 编译结果移动到原始py文件对应位置
3. 删除原py文件 (可指定)
"""
import os
import py_compile


def process_file_or_directory(path, delete_original=True):
    """
    编译 -> 移动 -> 删除
    :param path: 目录/文件绝对路径
    :param delete_original: 是否删除源文件
    :return:
    """
    if os.path.isfile(path):
        if path.endswith('.py'):
            pyc_file_path = path[:-3] + '.pyc'
            try:
                # 编译Python文件
                py_compile.compile(path, pyc_file_path, doraise=True)

                # 根据参数决定是否删除原始的.py文件
                if delete_original:
                    os.remove(path)

                print(f"Processed {path}")
            except py_compile.PyCompileError as e:
                print(f"Error compiling {path}: {e}")
            except OSError as e:
                print(f"OS error occurred while processing {path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while processing {path}: {e}")
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    py_file_path = os.path.join(root, file)
                    process_file_or_directory(py_file_path, delete_original)
    else:
        print(f"Skipping non-Python file or invalid path: {path}")


def process_files_and_directories(paths, delete_original=True):
    for path in paths:
        process_file_or_directory(path, delete_original)

if __name__ == "__main__":
    # 处理指定目录, 文件夹或者单个py文件
    directory_list = [
        os.path.join(os.getcwd(), "tools"),
        r"D:\workspace\python_web_learn\funboost_test\2.py"
    ]

    # 是否删除原python文件 谨慎选择
    delete_original = False

    process_files_and_directories(directory_list, delete_original)