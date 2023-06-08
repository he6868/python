# -*- coding:utf-8 -*-
# @time :2023-6-4 13:27
# @Author :lemon_huahua
# @File: txt_tool.py
# 文件说明：txt文件管理工具

class TxtTool:

    # 写入txt文件
    def write_txt(self, file_path, value, write_mode='a'):
        """
        :param file_path: txt文件路径
        :param write_mode: 写入模式，默认是a(追加模式)
        :param value: 写入的内容
        :return:
        """
        with open(file_path, write_mode, encoding='utf-8') as f:
            f.write(value)
