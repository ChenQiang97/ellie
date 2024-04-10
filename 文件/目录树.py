import re
from pathlib import Path


def scan_file_new(path: str) -> list:
    """
    扫描目录, 获取目录树 例如: elmentUI 多级目录
    :param path: root path
    :return:
    """
    items = Path(path).iterdir()
    subFiles = []
    for item in items:
        v = str(item).replace(str(path), '')
        subResult = []
        if item.is_dir():
            subResult = scan_file_new(str(item))
        if item.is_dir():
            subFiles.insert(0, {
                # 去掉开头的斜杠 win: \ linux:/
                "label": re.sub('^/|\\\\', '', v),
                "path": str(item),
                "is_dir": item.is_dir(),
                "children": subResult
            })
        else:
            subFiles.append({
                # 去掉开头的斜杠 win: \ linux:/
                "label": re.sub('^/|\\\\', '', v),
                "path": str(item),
                "is_dir": item.is_dir(),
                "children": subResult
            })

    return subFiles


if __name__ == '__main__':
    print(scan_file_new(r"D:\workspace\ellie"))
