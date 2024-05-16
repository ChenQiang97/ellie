# 连接到MongoDB数据库
import datetime
import random
import uuid

import mongoengine

from taptap.模型 import Report

mongoengine.connect('core', host='192.168.192.188', port=27017)

# 选择数据库和集合
db = mongoengine.get_db()
collection = db.reports


def generate_test_data():
    items = []
    for i in range(100):
        item = {
            "report_id": str(uuid.uuid4()),
            "report_name": f"Report {i}",
            "data_id": f"data_{i}",
            # 工具版本号
            "tool_version": random.choice(["v1.0", "v1.1", "v1.2", "v1.3", "v1.4"]),
            # 正确率
            "accuracy": random.random(),
            # 误触数量
            "false_positive": random.randint(0, 100),
            # 总数
            "total": random.randint(100, 1000),
            # 成功识别数量
            "success": random.randint(0, 100),
            # 创建时间
            "create_time": datetime.datetime.now(),
            "result": {}
        }
        for i in range(1, 25):
            item["result"][f"AP{i}"] = {
                "accuracy": random.random(),
                "total": random.randint(100, 1000),
                "success": random.randint(0, 100)
            }
        item["result"]["AP_ALL"] = {
            "accuracy": random.random(),
            "total": random.randint(100, 1000),
            "success": random.randint(0, 100)
        }

        for i in range(1, 11):
            item["result"][f"AN{i}"] = {
                "false_positive": random.randint(0, 100)
            }
        item["result"]["AN_ALL"] = {
            "false_positive": random.randint(0, 100)
        }
        items.append(item)
        Report(**item).save()
        print(item)

generate_test_data()