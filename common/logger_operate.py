# -*- coding:utf-8 -*-
# @time :2023-5-20 14:33
# @Author :lemon_huahua
# @File: logger_operate.py
# 文件说明：日志操作
import datetime
import os

from common.base import Base
from common.edit_file_tool.txt_tool import TxtTool


class Logger:

    # 测试用例日志化
    def test_case_log(self, *data):
        """
        用于将（全局变量）替换后的测试用例输入的txt日志文件，方便调试
        :param case_data: （全局变量）替换后的测试用例数据。单条
        :return:
        """
        # 获取当前时间
        time_ = datetime.datetime.now()
        # excel文件名、sheet页名称、用例所在行数
        excel_name,sheet_name,row_num = os.path.basename(data[0][-1][0]),data[0][-1][1],data[0][-1][2]
        # 请求方法、请求url、请求头、请求体、接口响应码、接口响应信息
        mode, url_, head, body, code_, info_ = data[1], data[2], data[3], data[4], data[5][0], data[5][1]

        # 定义写入内容
        valeus = f"""\n
【执行时间】：{time_}
【执行文件名】：{excel_name}
【sheet页名称】：{sheet_name}
【用例所在行数】：{row_num}
【请求方法】：{mode}
【请求url】：{url_}
【请求头】：{head}
【请求体】：{body}
【接口响应码】：{code_}
【接口响应信息】：{info_}
------------------------------------------------------------------------------------------------------------------------
        """
        # 将日志写入txt文件
        TxtTool().write_txt(f'{Base().get_project_path()}/data/config_data/log.txt', valeus)

# for i in ExcelRelated().format_excel_data():
#     print(i)
