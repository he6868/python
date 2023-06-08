# -*- coding:utf-8 -*-
# @time :2023-4-26 23:26
# @Author :lemon_huahua
# @File: read_case.py
# 文件说明：用例读取类
import glob
import os
from common.base import Base
from common.edit_file_tool.excel_tool import ExcelTool


class ReadCase:

    def __init__(self):
        # 定义读取excel路径
        self.excel_path = fr'{Base().get_project_path()}/data/case_data'

    # excel用例文件优先级定义：用于定义（前置用例、后置用例）的读取顺序
    def case_excel_priority_definition(self):
        """
        可以遍历父级目录以及子级目录，每个目录都按照相同的规则进行排序
        :return: 返回一个排序好的列表
        """
        # 获取读取目录
        cases_dir = self.excel_path
        # 使用 glob.glob 搜索目录下的所有 .xlsx 文件
        xlsx_files = glob.glob(os.path.join(cases_dir, '**/test*.xlsx'), recursive=True)
        case_set_dict = {}  # 用于存储排序好的excel路径

        # 遍历每个文件，获取其所在目录名称并打印
        for xlsx_file in xlsx_files:
            # 通过.xlsx路径获取其所在（目录名称）
            dir_name = os.path.basename(os.path.dirname(xlsx_file))
            # 如果key已经存在于字典中
            if dir_name in case_set_dict:
                case_set_dict[dir_name].append(xlsx_file)  # 则将值添加到列表中
            else:
                case_set_dict.setdefault(dir_name, [xlsx_file])  # 否则添加新的键值对

        # 对字典进行遍历，通过key同时获取其value
        for directory, case_file_list in case_set_dict.items():
            # 对文件进行排序处理：将（前置用例）调序到前面，（后置用例）调序到末尾
            for file_path in case_file_list:
                if '前置用例' in file_path:  # 将（前置用例）排在列表第一位
                    case_file_list.remove(file_path)  # 在列表中将它移除
                    case_file_list.insert(0, file_path)  # 然后在列表0下标位置添加它
                if '后置用例' in file_path:  # 将（后置用例）排在列表末尾
                    case_file_list.remove(file_path)  # 在列表中将它移除
                    case_file_list.append(file_path)  # 然后在列表末尾添加它
            # 将排序好的规则重新赋值到字典中
            case_set_dict[directory] = case_file_list

        # 整理一个排序好的列表：方便后续遍历执行
        cases_set = []  # 用于存储整理排序后的用例文件路径
        for value_ in case_set_dict.values():
            for case_file_path in value_:
                cases_set.append(case_file_path)
        # 返回排列好的列表
        return cases_set

    # 格式化excel成用例数据，方便后续执行
    def read_case(self):
        """
        指定目录读取excel，将读取出来的excel格式化成用例结构，方便后续调用
        :return: excel用例数据
        """
        # 获取用例文件路径（已经经过排序）
        case_file_path = self.case_excel_priority_definition()
        test_case = []  # 用于存储调试用例
        case_set = []  # 用于存储用例

        # 遍历目录下所有excel文件路径
        for excel_file in case_file_path:
            # 以路径来读取excel文件
            case_group = ExcelTool().read_excel(excel_file)
            # 遍历用例里面的每一行数据
            for case_data in case_group:
                # 调试用：如果（前置条件）填写“调试”二字，则只运行该用例
                if case_data[4] == '调试':
                    test_case.append(case_data)

                # 排除（关键字）为空的用例，和排除表头为“用例编号”的数据
                elif case_data[6] and case_data[0] != '用例编号':
                    case_set.append(case_data)
        # 如果（调试用例）不为空则返回
        if test_case:
            return test_case
        return case_set