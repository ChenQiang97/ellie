# 多版本报告

import random

import pandas as pd

from taptap.test_data import multi_version_success_rate_data, version_list, multi_version_fail_data, \
    single_version_success_rate_data, single_version_fail_data


# 单版本成功率
def single_version_success_rate(writer, data, sheet_name):
    df = pd.DataFrame(data)

    df['successRate'] = (df['successRate'] * 100).round(2).astype(str) + '%'

    print(df.shape)
    new_columns = ['id', 'motion_scene', 'orientation', 'grip_pose', 'hit_position', 'name', 'successCount',
                   'totalCount',
                   'successRate']

    # 调整列顺序
    df = df[new_columns]
    df.columns = ['id', '动作场景', '屏幕方向', '握手姿势', '敲击位置', '数据采集记录编号', '成功次数', '总次数',
                  '成功率']

    # 添加表头 行
    item = {}
    for i in df.columns:
        item[i] = i
    new_row = pd.DataFrame(item, index=[0])
    df = pd.concat([new_row, df]).reset_index(drop=True)

    df.to_excel(writer, index=False, header=False, sheet_name=sheet_name)

    worksheet = writer.sheets[sheet_name]

    workbook = writer.book
    format_center = workbook.add_format({
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    # set excel header format
    header_fmt = workbook.add_format({
        'bold': True,
        'fg_color': '#D7E4BC',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    tail_fmt = workbook.add_format({
        'bold': True,
        'fg_color': '#4bb4d1',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    # 写入表头
    for index, row in df.iterrows():
        print(index, row)
        if index == 0:
            for col_num, value in enumerate(row.values):
                if pd.isna(value):
                    worksheet.write(0, col_num, "", header_fmt)
                else:
                    worksheet.write(0, col_num, value, header_fmt)
        else:
            for col_num, value in enumerate(row.values):
                if pd.isna(value):
                    worksheet.write(index, col_num, "", format_center)
                else:
                    worksheet.write(index, col_num, value, format_center)

    worksheet.set_column(0, 2, 10, format_center)
    worksheet.set_column(3, 3, 30, format_center)
    worksheet.set_column(4, 100, 15, format_center)

    # 合并指定列单元格
    target_column_list = ['id', '动作场景', '屏幕方向', '握手姿势']
    for target_column in target_column_list:
        # 获取列号
        column_index = df.columns.get_loc(target_column)
        tmp_value = None
        start_row = None
        # 遍历指定列， 获取行号
        for row_num, value in enumerate(df[target_column][1:]):
            if pd.isna(value):
                value = ""
            if start_row is None:
                tmp_value = value
                start_row = row_num + 1
            if value != tmp_value:
                end_row = row_num
                # 合并单元格
                print(start_row, column_index, end_row, column_index, tmp_value)
                parm = (start_row, column_index, end_row, column_index, tmp_value)
                if start_row != end_row:
                    worksheet.merge_range(start_row, column_index, end_row, column_index, tmp_value)

                tmp_value = value
                start_row = row_num + 1

            # print(target_column, row_num+1, column_index, value)

    print(df.head(20))

    print(df.shape)

    # 合并最后一行单元格
    worksheet.merge_range(df.shape[0] - 1, 0, df.shape[0] - 1, 5, "all", tail_fmt)

    # 设置边框
    border_fmt = workbook.add_format({'bottom': 1, 'top': 1, 'left': 1, 'right': 1})
    worksheet.conditional_format(0, 0, len(df) - 1, len(df.columns) - 1,
                                 {'type': 'no_errors', 'format': border_fmt})


# 单版本失败率
def single_version_fail_rate(writer, data, sheet_name):
    df = pd.DataFrame(data)

    print(df.shape)
    new_columns = ['id', 'motion_scene', 'name', 'error_count']

    # 调整列顺序
    df = df[new_columns]
    df.columns = ['id', '动作场景', '测试名称', '错误次数']

    df.to_excel(writer, index=False, sheet_name=sheet_name)

    worksheet = writer.sheets[sheet_name]

    workbook = writer.book
    format_center = workbook.add_format({
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    # set excel header format
    header_fmt = workbook.add_format({
        'bold': True,
        'fg_color': '#D7E4BC',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    tail_fmt = workbook.add_format({
        'bold': True,
        'fg_color': '#4bb4d1',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    for col_num, value in enumerate(df.columns.values):
        # 判断 nan 值，并设置单元格格式
        if pd.isna(value):
            worksheet.write(0, col_num, "", header_fmt)
        else:
            worksheet.write(0, col_num, value, header_fmt)

    # 获取df的最后一行的内容
    for col_num, value in enumerate(df.tail(1).values[0].tolist()):
        print(col_num, value)
        # 写入最后一行
        if pd.isna(value):
            worksheet.write(df.shape[0], col_num, "", tail_fmt)
        else:
            worksheet.write(df.shape[0], col_num, value, tail_fmt)

    # 设置列宽
    worksheet.set_column(0, 0, 10, format_center)
    worksheet.set_column(1, 1, 70, format_center)
    worksheet.set_column(2, 5, 10, format_center)

    # 合并最后一行单元格
    worksheet.merge_range(df.shape[0], 0, df.shape[0], 2, "all", tail_fmt)

    # 设置边框
    border_fmt = workbook.add_format({'bottom': 1, 'top': 1, 'left': 1, 'right': 1})
    worksheet.conditional_format(0, 0, len(df), len(df.columns) - 1,
                                 {'type': 'no_errors', 'format': border_fmt})


# 多版本成功率
def multi_version_success_rate(writer, data, version_list, sheet_name):
    df = pd.DataFrame(data)

    print(df.shape)

    # 调整前6列顺序
    new_columns = ['id', 'motion_scene', 'orientation', 'grip_pose', 'hit_position', 'name']
    for column in df.columns[6:]:
        new_columns.append(column)
    print(new_columns)
    df = df[new_columns]

    # df.columns = ['id', '动作场景', '屏幕方向', '握手姿势', '敲击位置', '测试名称', '成功次数', '总次数', '成功率']

    print(df.columns)
    # 添加表头 行
    item = {}
    for i in df.columns:
        item[i] = i
    new_row = pd.DataFrame(item, index=[0])
    df = pd.concat([new_row, df]).reset_index(drop=True)

    item = {}
    for key, value in df.iloc[1].to_dict().items():
        item[key] = key
        for version in version_list:
            if version in key:
                item[key] = version

    new_row = pd.DataFrame(item, index=[0])
    df = pd.concat([new_row, df]).reset_index(drop=True)

    for index, row in df.iterrows():
        if index <= 1:
            for col_num, value in enumerate(row.values):
                if value == "motion_scene":
                    df.at[index, value] = "动作场景"
                elif value == "orientation":
                    df.at[index, value] = "屏幕方向"
                elif value == "grip_pose":
                    df.at[index, value] = "握手姿势"
                elif value == "hit_position":
                    df.at[index, value] = "敲击位置"
                elif value == "name":
                    df.at[index, value] = "数据采集(记录编号)"

    print(df.head(20))

    df.to_excel(writer, index=False, header=False, sheet_name=sheet_name)

    worksheet = writer.sheets[sheet_name]

    workbook = writer.book
    format_center = workbook.add_format({
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    # set excel header format
    header_fmt = workbook.add_format({
        'bold': True,
        'bg_color': '#D7E4BC',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    tail_fmt = workbook.add_format({
        'bold': True,
        'fg_color': '#4bb4d1',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    # 写入数据
    for index, row in df.iterrows():

        for col_num, value in enumerate(row.values):
            if index == 1:
                if "successCount" in value:
                    value = "成功次数"
                elif "totalCount" in value:
                    value = "总次数"
                elif "successRate" in value:
                    value = "成功率"

            if pd.isna(value):
                worksheet.write(index, col_num, "", format_center)
            else:
                worksheet.write(index, col_num, value, format_center)

    worksheet.set_column(0, 2, 10, format_center)
    worksheet.set_column(3, 3, 30, format_center)
    worksheet.set_column(4, 100, 15, format_center)

    # 合并指定列单元格
    target_column_list = ['grip_pose', 'id', 'motion_scene', 'orientation', 'name', 'hit_position']
    for target_column in target_column_list:
        # 获取列号
        column_index = df.columns.get_loc(target_column)
        tmp_value = None
        start_row = None
        # 遍历指定列， 获取行号
        for row_num, value in enumerate(df[target_column]):
            if pd.isna(value):
                value = ""
            if start_row is None:
                tmp_value = value
                start_row = row_num
            if value != tmp_value:
                end_row = row_num - 1
                # 合并单元格
                print(start_row, column_index, end_row, column_index, tmp_value)
                parm = (start_row, column_index, end_row, column_index, tmp_value)
                if start_row != end_row:
                    worksheet.merge_range(start_row, column_index, end_row, column_index, tmp_value)

                tmp_value = value
                start_row = row_num

    # 合并第一行单元格 版本号
    for index, row in df.iterrows():
        if index == 0:
            tmp_value = None
            start_col = None
            for col_num, value in enumerate(row.values):
                if pd.isna(value):
                    value = ""
                if start_col is None:
                    tmp_value = value
                    start_col = col_num
                if value != tmp_value:
                    end_col = col_num - 1
                    # 合并单元格
                    print(0, start_col, 0, end_col, tmp_value)
                    parm = (0, start_col, 0, end_col, tmp_value)
                    if start_col != end_col:
                        worksheet.merge_range(0, start_col, 0, end_col, tmp_value)

                    tmp_value = value
                    start_col = col_num
                # 判断是不是最后一列
                if col_num == len(row.values) - 1:
                    end_col = col_num
                    # 合并单元格
                    print(0, start_col, 0, end_col, tmp_value)
                    parm = (0, start_col, 0, end_col, tmp_value)
                    if start_col != end_col:
                        worksheet.merge_range(0, start_col, 0, end_col, tmp_value)
            break

    # 合并最后一行单元格
    worksheet.merge_range(df.shape[0] - 1, 0, df.shape[0] - 1, 5, "all", tail_fmt)

    # 设置边框
    border_fmt = workbook.add_format({'bottom': 1, 'top': 1, 'left': 1, 'right': 1})
    worksheet.conditional_format(0, 0, len(df) - 1, len(df.columns) - 1,
                                 {'type': 'no_errors', 'format': border_fmt})
    #
    # 表头
    worksheet.conditional_format(0, 0, 1, 5, {'type': 'no_errors', 'format': header_fmt})
    color_list = ['#ded3a6', '#83afde', '78de98', '#d8abde']
    for index, version in enumerate(version_list):
        version_header_fmt = workbook.add_format({
            'bold': True,
            'bg_color': random.choice(color_list),
            'border': 1,
            'text_wrap': True,
            "align": "center",
            "valign": "vcenter",
            "font_name": "微软雅黑",
        })
        start_col = 6 + index * 3
        print(0, start_col, 1, start_col + 2)
        worksheet.conditional_format(0, start_col, 1, start_col + 2,
                                     {'type': 'no_errors', 'format': version_header_fmt})

    #
    # red_format = workbook.add_format({'bg_color': '#FF0000'})
    #
    # # 添加条件格式规则：如果单元格的值等于20，则应用红色背景
    # worksheet.conditional_format(0, 0, len(df) - 1, len(df.columns) - 1, {'type': 'cell',
    #                                                'criteria': '>=',
    #                                                'value': 20,
    #                                                'format': red_format})


# 多版本失败率
def multi_version_fail_rate(writer, data, version_list, sheet_name):
    df = pd.DataFrame(data)

    print(df.shape)
    new_columns = ['id', 'motion_scene', 'name']
    for column in df.columns[3:]:
        new_columns.append(column)
    print(new_columns)
    df = df[new_columns]

    # 添加表头 行
    item = {}
    for i in df.columns:
        item[i] = i
    new_row = pd.DataFrame(item, index=[0])
    df = pd.concat([new_row, df]).reset_index(drop=True)

    item = {}
    for key, value in df.iloc[1].to_dict().items():
        item[key] = key
        for version in version_list:
            if version in key:
                item[key] = version
    new_row = pd.DataFrame(item, index=[0])
    df = pd.concat([new_row, df]).reset_index(drop=True)

    for index, row in df.iterrows():
        if index <= 1:
            for col_num, value in enumerate(row.values):
                if value == "motion_scene":
                    df.at[index, value] = "动作场景"
                elif value == "name":
                    df.at[index, value] = "数据采集(记录编号)"

    df.to_excel(writer, index=False, header=False, sheet_name=sheet_name)
    worksheet = writer.sheets[sheet_name]

    workbook = writer.book
    format_center = workbook.add_format({
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    # set excel header format
    header_fmt = workbook.add_format({
        'bold': True,
        'bg_color': '#D7E4BC',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    tail_fmt = workbook.add_format({
        'bold': True,
        'fg_color': '#4bb4d1',
        'border': 1,
        'text_wrap': True,
        "align": "center",
        "valign": "vcenter",
        "font_name": "微软雅黑",
    })

    # 写入数据
    for index, row in df.iterrows():

        for col_num, value in enumerate(row.values):
            if index == 1:
                if "error_count" in value:
                    value = "误触次数"

            if pd.isna(value):
                worksheet.write(index, col_num, "", format_center)
            else:
                worksheet.write(index, col_num, value, format_center)

    # 设置列宽
    worksheet.set_column(0, 0, 10, format_center)
    worksheet.set_column(1, 1, 70, format_center)
    worksheet.set_column(2, 2, 25, format_center)
    worksheet.set_column(3, 5, 15, format_center)

    # 合并指定列单元格
    target_column_list = ['id', 'motion_scene', 'name']
    for target_column in target_column_list:
        # 获取列号
        column_index = df.columns.get_loc(target_column)
        tmp_value = None
        start_row = None
        # 遍历指定列， 获取行号
        for row_num, value in enumerate(df[target_column]):
            if pd.isna(value):
                value = ""
            if start_row is None:
                tmp_value = value
                start_row = row_num
            if value != tmp_value:
                end_row = row_num - 1
                # 合并单元格
                print(start_row, column_index, end_row, column_index, tmp_value)
                parm = (start_row, column_index, end_row, column_index, tmp_value)
                if start_row != end_row:
                    worksheet.merge_range(start_row, column_index, end_row, column_index, tmp_value)

                tmp_value = value
                start_row = row_num

    # 合并最后一行单元格
    worksheet.merge_range(df.shape[0] - 1, 0, df.shape[0] - 1, 2, "all", tail_fmt)

    # 设置边框
    border_fmt = workbook.add_format({'bottom': 1, 'top': 1, 'left': 1, 'right': 1})
    worksheet.conditional_format(0, 0, len(df) - 1, len(df.columns) - 1,
                                 {'type': 'no_errors', 'format': border_fmt})
    #
    # 表头
    worksheet.conditional_format(0, 0, 1, 5, {'type': 'no_errors', 'format': header_fmt})

    color_list = ['#ded3a6', '#83afde', '78de98', '#d8abde']
    for index, version in enumerate(version_list):
        version_header_fmt = workbook.add_format({
            'bold': True,
            'bg_color': random.choice(color_list),
            'border': 1,
            'text_wrap': True,
            "align": "center",
            "valign": "vcenter",
            "font_name": "微软雅黑",
        })
        start_col = 3 + index
        print(0, start_col, 1, start_col)
        worksheet.conditional_format(0, start_col, 1, start_col,
                                     {'type': 'no_errors', 'format': version_header_fmt})


writer = pd.ExcelWriter('taptap_test.xlsx', engine='xlsxwriter')

multi_version_success_rate(writer, multi_version_success_rate_data, version_list, "多版本成功率")

multi_version_fail_rate(writer, multi_version_fail_data, version_list, "多版本失败率")

single_version_success_rate(writer, single_version_success_rate_data, "单版本成功率")

single_version_fail_rate(writer, single_version_fail_data, "单版本失败率")

writer.close()
