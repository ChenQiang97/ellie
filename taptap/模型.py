import mongoengine

class Report(mongoengine.Document):
    meta = {
        'collection': 'reports'
    }
    report_id = mongoengine.StringField(required=True, unique=True)  # `
    report_name = mongoengine.StringField(required=True)  # 报告名称
    data_id = mongoengine.StringField(required=True)  # 数据ID
    tool_version = mongoengine.StringField(required=True)  # 工具版本号
    accuracy = mongoengine.FloatField(required=True)  # 正确率
    false_positive = mongoengine.IntField(required=True)  # 误触数量
    total = mongoengine.IntField(required=True)  # 总数
    success = mongoengine.IntField(required=True)  # 成功识别数量
    create_time = mongoengine.DateTimeField(required=True)
    # 结果字典
    result = mongoengine.DictField()

    is_deleted = mongoengine.IntField(default=0)