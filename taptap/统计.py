"""
需求:
数据度量: 饼图四选二
所有报告列表

指定版本之间四个值的对比: 针对单条数据

(柱状图) 全版本平均指标对比 不同版本数据(指定或者全部), 正确率, 误触, 总数, 成功识别 均值 数量对比  x: 版本, y: 值
"""

import datetime
import random
import uuid
from functools import reduce

import mongoengine


class Report(mongoengine.Document):
    meta = {
        'collection': 'reports'
    }
    report_id = mongoengine.StringField(required=True, unique=True) #`
    report_name = mongoengine.StringField(required=True) # 报告名称
    data_id = mongoengine.StringField(required=True) # 数据ID
    tool_version = mongoengine.StringField(required=True) # 工具版本号
    accuracy = mongoengine.FloatField(required=True)    # 正确率
    false_positive = mongoengine.IntField(required=True)    # 误触数量
    total = mongoengine.IntField(required=True) # 总数
    success = mongoengine.IntField(required=True) # 成功识别数量
    create_time = mongoengine.DateTimeField(required=True)

    is_deleted = mongoengine.IntField(default=0)


# 连接到MongoDB数据库
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
            "create_time": datetime.datetime.now()
        }
        items.append(item)
        Report(**item).save()
        print(item)


#
# generate_test_data()

tool_version_list = ["v1.2", "v1.3", "v1.4"]
data_id_list = []

for tool_version in tool_version_list:
    tool_version_data_id_list = list(Report.objects(tool_version=tool_version).distinct("data_id"))
    if tool_version_data_id_list:
        data_id_list.append(tool_version_data_id_list)
    print(f"tool_version: {tool_version}, data_id: {tool_version_data_id_list}")

print(data_id_list)
# 函数: 子列表取交集
def get_common_data_id(data_id_list):
    """
    注意: 需要确保子列表不为空
    :param data_id_list:
    :return:
    """
    if not data_id_list:
        return []

    # 使用 reduce 和集合的交集方法来找到所有列表的共同元素
    common_data_id = reduce(set.intersection, (set(data_id) for data_id in data_id_list))

    # 将集合转回列表并返回
    return list(common_data_id)

common_data_id = get_common_data_id(data_id_list)

reposts = list(Report.objects(is_deleted=0, data_id__in=common_data_id).aggregate([
    {
        "$project": {
            "_id": 0,
            "report_id": 1,
            "report_name": 1,
            "data_id": 1,
            "tool_version": 1,
            "accuracy": 1,
            "false_positive": 1,
            "total": 1,
            "success": 1,
            "create_time": 1
        }
    }
]))

for data_id in common_data_id:
    item = {
        "data_id": data_id,
        "accuracy":{},
        "false_positive":{},
        "total":{},
        "success":{}
    }
    for repost in reposts:
        if repost["data_id"] == data_id:
            tool_version = repost["tool_version"]
            if tool_version not in tool_version_list:
                continue
            item["accuracy"][tool_version] = repost["accuracy"]
            item["false_positive"][tool_version] = repost["false_positive"]
            item["total"][tool_version] = repost["total"]
            item["success"][tool_version] = repost["success"]


    print(item)



# 统计各版本工具的平均正确率和平均误触数量
pipeline = [
    {
        "$group": {
            "_id": "$tool_version",  # 分组字段
            "avg_accuracy": {"$avg": "$accuracy"},  # 计算success的平均值
            "avg_false_positive": {"$avg": "$false_positive"}  # 计算false_positive的平均值
        }
    }
]

# 执行聚合查询
results = Report.objects.aggregate(*pipeline)

# 打印结果
for result in results:
    print(
        f"Tool Version: {result['_id']}, Average Accuracy: {result['avg_accuracy']}, Average False Positives: {result['avg_false_positive']}")
