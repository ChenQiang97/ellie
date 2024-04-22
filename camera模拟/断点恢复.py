"""
使用断点恢复的方式，编写一个Python脚本，该脚本能够模拟执行push操作。
在执行过程中，能够记录已经执行过的目录，并在下次执行时，从上一次中断的位置继续执行。
"""
import os
import time


# 模拟执行push操作
def push_directory(directory):
    try:
        # 这里执行你的push操作，例如使用git或其他API
        print(f"Pushing directory {directory}")
        time.sleep(0.5)  # 模拟执行时间，这里假设10秒
        # 假设如果push成功，返回True；否则返回False
        return True
    except Exception as e:
        print(f"Push failed for directory {directory}: {e}")
        return False


def run():
    # 记录执行状态的文件路径
    state_file = "push_state.txt"

    # 读取执行状态
    pushed_directories_set = set()
    try:
        with open(state_file, "r") as f:
            lines = f.readlines()
            if lines and lines[-1].strip() == "end":
                print("All directories have been pushed. Exiting...")
                return
            pushed_directories_set = set([line.strip() for line in lines])
            print(f"Resuming from {len(pushed_directories_set)} directories...")
            print(pushed_directories_set)
    except FileNotFoundError:
        pass  # 文件不存在，说明之前没有执行过或者状态文件被删除了

    # 遍历目录
    root_dir = "data_folders"
    for action in os.listdir(root_dir):
        # 跳过非目录文件
        if os.path.isfile(os.path.join(root_dir, action)):
            continue
        for dirpath in os.listdir(os.path.join(root_dir, action)):
            # 跳过已经执行过的目录
            if dirpath in pushed_directories_set:
                print(f"Skipping directory {dirpath} as it has already been pushed")
                continue
            success = push_directory(os.path.join(root_dir, action, dirpath))
            if success:
                with open(state_file, "a") as f:  # 使用追加模式写入
                    f.write(dirpath + "\n")
            else:
                print(f"Skipping directory {dirpath} due to push failure")

    with open(state_file, "a") as f:  # 追加"end"表示任务完成
        f.write("end\n")


if __name__ == "__main__":
    run()
