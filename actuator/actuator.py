# -*- coding:utf-8 -*-
# @time :2023-5-13 22:12
# @Author :lemon_huahua
# @File: actuator.py
# 文件说明：总执行器
import time
from common.read_case import ReadCase
from key_word.key_word import Key
from common.base import Base
from common.edit_file_tool.txt_tool import TxtTool


class Actuator:

    # 前置处理器
    def __init__(self):
        # 清空txt日志文件内容
        TxtTool().write_txt(rf'{Base().get_project_path()}/data/config_data/log.txt', '', 'w')

    # 执行器
    def actuator(self):
        str_time = time.time()  # 统计开始时间
        case_set = ReadCase().read_case()  # 读取用例：将用例一次性全部提取出来

        for case_data in case_set:  # 循环执行用例
            case_data = Key().global_var_replace(case_data)  # 将每条用例的全局变量替换
            key_word = case_data[6]  # 从excel中提取关键字
            ret = getattr(Key(),key_word)(case_data)  # 调用关键字库，并执行用例

        # 计算执行用例总耗时
        end_time = time.time()
        print(f'用例执行完成，总耗时{end_time-str_time}')


Actuator().actuator()
