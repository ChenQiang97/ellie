"""
超大文件读取
当文件过大时，需要采用分块读取的方式，避免一次性读取整个文件导致内存溢出。
"""

# v1.0 当文件单行过长时，可能会导致内存溢出，因此改用分块读取
from functools import partial


def retrun_count(fname):
    """计算文件有多少行
    """
    count = 0
    with open(fname) as file:
        for line in file:
            count += 1
    return count


# v2.0 改进版，使用分块读取，每次读取 8KB 内容，直到文件结束
def return_count_v2(fname):
    count = 0
    block_size = 1024 * 8
    with open(fname) as fp:
        while True:
            chunk = fp.read(block_size)
            # 当文件没有更多内容时，read 调用将会返回空字符串 ''
            if not chunk:
                break
            count += 1
    return count


# v3.0 改进版，使用生成器函数，每次读取 8KB 内容，直到文件结束
def chunked_file_reader(fp, block_size=1024 * 8):
    """生成器函数：分块读取文件内容
    """
    while True:
        chunk = fp.read(block_size)
        # 当文件没有更多内容时，read 调用将会返回空字符串 ''
        if not chunk:
            break
        yield chunk

def return_count_v3(fname):
    count = 0
    with open(fname) as fp:
        for chunk in chunked_file_reader(fp):
            count += 1
    return count


# v4.0 改进版，使用生成器函数，每次读取 8KB 内容，直到文件结束，使用 iter 函数
def chunked_file_reader_v2(file, block_size=1024 * 8):
    """生成器函数：分块读取文件内容，使用 iter 函数
    """
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    # 循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    for chunk in iter(partial(file.read, block_size), ''):
        yield chunk