"""
从URL地址提取文件名，并下载文件: 分块写入文件
"""
import os
import time
from urllib.parse import unquote
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


# 获取文件名
def get_file_name(url, headers):
    filename = ''
    if 'Content-Disposition' in headers and headers['Content-Disposition']:
        disposition_split = headers['Content-Disposition'].split(';')
        if len(disposition_split) > 1:
            if disposition_split[1].strip().lower().startswith('filename='):
                file_name = disposition_split[1].split('=')
                if len(file_name) > 1:
                    filename = unquote(file_name[1])
    if not filename and os.path.basename(url):
        filename = os.path.basename(url).split("?")[0]
    if not filename:
        return time.time()
    return filename


# 下载文件: 分块写入文件
def download_file(response, file_name):
    with open(file_path + file_name, "wb") as pyFile:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pyFile.write(chunk)
    print('下载完成')


# 开始下载
def start(url):
    response = requests.get(url=url, headers=headers, stream=True, allow_redirects=False, timeout=10)
    content_length = response.headers['Content-Length']  # Transfer-Encoding:chunked时为块传输，无content_length
    file_name = get_file_name(url, response.headers)
    download_file(response, file_name)
    print("文件大小：", content_length, "文件名称：" + file_name)


if __name__ == '__main__':
    file_path = 'C:\\xx\down\\'
    url = 'https://iterm2.com/downloads/stable/iTerm2-3_3_6.zip'

    start(url)
