def get_tail(file: str, taillines: int = 500, return_str: bool = True, avg_line_length: int = None) -> str:
    """
    读取大文件倒数指定行数
    :param file: 文件名
    :param taillines: 读取的行数
    :param return_str: 返回格式 默认字符串 可选(字符串 OR 列表)
    :param avg_line_length: 每行字符平均数
    :return:
    """
    with open(file, errors='ignore') as f:
        if not avg_line_length:
            f.seek(0, 2)
            f.seek(f.tell() - 3000)
            avg_line_length = int(3000 / len(f.readlines())) + 10
        f.seek(0, 2)
        end_pointer = f.tell()
        offset = taillines * avg_line_length
        if offset > end_pointer:
            f.seek(0, 0)
            lines = f.readlines()[-taillines:]
            return "".join(lines) if return_str else lines
        offset_init = offset
        i = 1
        while len(f.readlines()) < taillines:
            location = f.tell() - offset
            f.seek(location)
            i += 1
            offset = i * offset_init
            if f.tell() - offset < 0:
                f.seek(0, 0)
                break
        else:
            f.seek(end_pointer - offset)
        lines = f.readlines()
        if len(lines) >= taillines:
            lines = lines[-taillines:]

        return "".join(lines) if return_str else lines