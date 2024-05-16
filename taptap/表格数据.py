import json
from functools import reduce

import mongoengine

from taptap.模型 import Report

mongoengine.connect('core', host='192.168.192.188', port=27017)

# 选择数据库和集合
db = mongoengine.get_db()
collection = db.reports

tool_version_list = ["v1.2", "v1.3", "v1.4"]
data_id_list = []

item = {
    "data_id": "123",
    "flode_shope": "折叠",
    "tool_version_list": ["v1.2", "v1.3", "v1.4"],
    "dataList": []
}

group = {"_id": None}

for i in range(1, 25):
    group[f"AP{i}_total"] = {"$sum": f"$result.AP{i}.total"}
    group[f"AP{i}_accuracy"] = {"$avg": f"$result.AP{i}.accuracy"}
    group[f"AP{i}_success"] = {"$sum": f"$result.AP{i}.success"}

group[f"APALL_total"] = {"$sum": f"$result.AP_ALL.total"}
group[f"APALL_accuracy"] = {"$avg": f"$result.AP_ALL.accuracy"}
group[f"APALL_success"] = {"$sum": f"$result.AP_ALL.success"}

for i in range(1, 11):
    group[f"AN{i}_false_positive"] = {"$sum": f"$result.AN{i}.false_positive"}

group[f"ANALL_false_positive"] = {"$sum": f"$result.AN_ALL.false_positive"}

data_list = []

for tool_version in tool_version_list:
    pipeline = [
        {
            "$group": group
        },
        {
            "$project": {
                "_id": 0
            }
        }
    ]
    report_list = list(Report.objects(tool_version=tool_version, is_deleted=0).aggregate(*pipeline))
    for report in report_list:
        print(report)
        row = {}
        for key, value in report.items():
            tmp = key.split("_")
            if tmp[0] not in row:
                row[tmp[0]] = {}
            row[tmp[0]]["".join(tmp[1:])] = value
        data_list.append(row)

print(json.dumps(data_list, indent=4))