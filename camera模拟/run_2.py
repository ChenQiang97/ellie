"""
tools/ -> /data/local/tmp/bm_test
xx.so -> /data/local/tmp/bm_test/libs : so
         /data/local/tmp/bm_test/output
modes -> /data/local/tmp/bm_test/models

2txt -> /data/local/tmp/bm_test/tools/res


act:
    1
        xx
        xx.txt
        yy
        yy.txt
    2
    3
    4
    5
    6
    7

1. 准备好环境，包括：
"""
import subprocess

# 删除/data/local/tmp/bm_test
# push models 版本
# push xx.so 版本
for xx in range(10):
    for yy in range(10):
        # 清空/data/local/tmp/bm_test/output
        # 清空/data/local/tmp/bm_test/input

        remote_dir = f"/act/{xx}/{yy}"
        local_dir = f"/{xx}/{yy}"
        # 检查远程目录是否存在的ADB命令
        check_cmd = ["adb", "shell", f"ls {remote_dir}"]
        # 推送目录的ADB命令
        push_cmd = ["adb", "push", local_dir, remote_dir]

        # 执行检查命令并获取输出
        result = subprocess.run(check_cmd, capture_output=True, text=True)

        # 如果远程目录不存在（命令返回非零退出码），则推送目录
        if result.returncode != 0:
            # push yy - > act/xx/yy
            # push yy.txt - > act/xx/yy
            print(f"Pushing {local_dir} to {remote_dir}...")
            subprocess.run(push_cmd)
        else:
            print(f"Directory {remote_dir} already exists on the device. Skipping push.")
        # 生成 俩txt
        # push input_txt_list.txt - > act/xx/yy
        # push input_vid_list.txt

        # 执行跑库

        # 拉取结果
        # pull output - > result



