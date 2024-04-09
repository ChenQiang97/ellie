import os
import py_compile
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog


def process_directory(directory, version):
    # 遍历指定目录下的所有Python文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                py_file_path = os.path.join(root, file)
                pyc_file_path = py_file_path + 'c'  # 临时.pyc文件路径

                # 编译Python文件
                py_compile.compile(py_file_path, pyc_file_path)

                # 形成正式的.pyc文件路径并移动文件
                final_pyc_path = py_file_path[:-3] + '.pyc'
                shutil.move(pyc_file_path, final_pyc_path)

                # 删除原始的.py文件
                os.remove(py_file_path)

                print(f"Processed {py_file_path}")

    print("All Python files in the specified directory have been compiled, moved, and the originals deleted.")
    return True


def write_compile_info(directory, version):
    compile_info = {
        'compile_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': version
    }

    info_file_path = os.path.join(directory, 'compile_info.txt')
    with open(info_file_path, 'w') as file:
        for key, value in compile_info.items():
            file.write(f"{key}: {value}\n")

    print(f"Compile info has been written to {info_file_path}")


def compile_files():
    version = version_entry.get()
    directory = directory_entry.get()

    if not os.path.isdir(directory):
        messagebox.showerror("错误", "指定的目录不存在！")
        return

    success = process_directory(directory, version)
    if success:
        write_compile_info(directory, version)
        messagebox.showinfo("编译成功", "Python文件已成功编译并删除，编译信息已保存。")
        # 编译成功后退出界面
        root.destroy()
    else:
        messagebox.showerror("编译失败", "编译过程中发生错误。")


# 创建主窗口
root = tk.Tk()
root.title("Python文件编译器")

# 创建并设置版本号输入框
tk.Label(root, text="版本号:").grid(row=0)
version_entry = tk.Entry(root)
version_entry.grid(row=0, column=1)

# 创建并设置目录输入框和选择目录按钮
tk.Label(root, text="指定目录:").grid(row=1)
directory_entry = tk.Entry(root)
directory_entry.grid(row=1, column=1)


def select_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)


select_button = tk.Button(root, text="选择目录", command=select_directory)
select_button.grid(row=1, column=2)

# 创建编译按钮
compile_button = tk.Button(root, text="编译", command=compile_files)
compile_button.grid(row=2, columnspan=2)

# 运行主循环
root.mainloop()
