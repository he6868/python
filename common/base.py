# -*- coding:utf-8 -*-
# @time :2023-5-10 12:48
# @Author :lemon_huahua
# @File: base.py
# 文件说明：基类
import json
import os
import re
import time
import urllib.parse
from jsonpath import jsonpath


class Base:

    # 获取项目根路径
    def get_project_path(self, project_name='pythonProject3'):
        # 获取当前文件的目录
        cur_path = os.path.abspath(os.path.dirname(__file__))
        # 获取项目根目录
        root_path = cur_path[:cur_path.find(project_name)] + f'{project_name}'
        return root_path

    # 中文符号转英文符号
    def symbol_conversion(self, conversion_str):
        """
        可以将字符串中的中文符号转换为英文符号
        :param conversion_info: 需要转换的字符串
        :return:
        """
        # 定义中文符号
        chinese_character = r'，。！？；：（）《》【】“”\‘\’、中文'
        # 定义对应的英文符号
        english_character = r',.!?;:()<>[]""\'\' 英文'
        table = conversion_str.maketrans(chinese_character, english_character)  # 创建转换表
        English_Symbols = conversion_str.translate(table)  # 进行转换
        return English_Symbols  # 返回转换信息

    # JsonPath提取器
    def json_path(self, data, json_paths):
        """
        :param data: 数据主体
        :param json_paths: jsonpath语法
        :return:
        """
        # 将传入的data数据扎转换为json格式
        json_data = json.loads(data)

        # 使用jsonpath语法提取数据,返回的是列表格式
        jsonpath_data = jsonpath(json_data, json_paths)

        if jsonpath_data:  # 判断json语法是否能获取到数据
            if len(jsonpath_data) == 1:  # 如果获取到的数据只有一个，则去除外括号返回
                return jsonpath_data[0]
            else:  # 否则则返回多组数据
                return jsonpath_data
        else:  # 如果json语法找不到数据，则直接返回None。必须是str格式，否则后续判断会报错
            return 'None'

    # 去除前后特定字符串
    def remove_before_after_string(self, string, before_str, after_str):
        """
        去除前后特定字符， 前面的字符和后面的字符都可以自定义
        :param string: 字符主体
        :param before_str: 需要去除前面的字符， 如果不存在则不去除
        :param after_str: 需要去除后面的字符，如果不存在则不去除
        :return:
        """
        prefix = before_str  # 需要去除前面的字符
        suffix = after_str  # 需要去除后面的字符
        if string.startswith(prefix):  # 判断是否是以特定字符开头
            string = string[len(prefix):]  # 是的话就去除
        if string.endswith(suffix):  # 判断是否是以特定字符结尾
            string = string[:-len(suffix)]  # 是的话就去除
        return string

    # 正则表达式提取器
    def regular_extractor(self, string, grammar):
        """
        :param string: 字符串主体
        :param grammar: 正则表达式语法
        :return:
        """
        pattern = grammar  # 定义正则表达式
        text = str(string)  # 获取字符串主体

        result = re.search(pattern, text)  # 匹配字符串

        if result:  # 如果能匹配到数据，则返回匹配结果
            return result.group(1)  # 返回匹配结果
        else:  # 如果匹配不到数据，则返回字符串None
            return 'None'

    # 可以根据用户输入的+-*/来计算
    def calculate_expression(self, expression):
        """
        对输入的表达式进行计算，并返回结果。
        :param expression: str, 用户输入的表达式，例如 "1 + 2 * 3"
        :return: float, 计算结果
        """
        try:
            # 将加减乘除运算符转换为对应的 Python 运算符
            operators = {
                '+': '+',
                '-': '-',
                '*': '*',
                '/': '/'
            }
            # 将表达式中的运算符替换成 Python 运算符
            for operator, python_operator in operators.items():
                expression = expression.replace(operator, python_operator)
            # 使用 Python 的 eval() 函数计算表达式并返回结果
            result = eval(expression)
            return str(result)
        except:  # 无法计算，请检查输入是否合法。
            return "None"

    # 断言类型判断
    def assertion_type_estimate(self, string):
        """
        用于区分（excel断言信息）中的前、中、后部分
        :param string: 断言数据
        :return: 返回是一个字典：front前、middle中、after后
        """
        separated_data = {'regular': 0}  # 用于存储分隔后断言数据：（regular）用于判断输入的是否是正则表达是，0表示不是
        string = string.strip()  # 去除前后空格

        # 循环（断言数据）中每个字符与其下标
        for index, value in enumerate(string[:-1]):
            # 如果字符中查询到']'括号，且后面第一个字符为（判断符号），则说明是最后一个列表括号
            if value in [']', '}'] and (string[index + 1]) in ['i', '=', '!', '>', '<']:

                # 【前面部分】：获取前面部分
                separated_data['front'] = (string[1:index]).strip()  # 获取（判断符号）前面部分，并去除其[]括号

                # 再次循环后面部分的
                for index2, value2 in enumerate(string[index + 1:]):
                    # 如果寻找到'['符号，则说明是（后面部分）的数据
                    if value2 in ['[']:
                        # 获取（判断符号）
                        separated_data['middle'] = string[index + 1:index + index2 + 1].strip()
                        # 获取判断符号（后面部分）。并去除其[]括号
                        separated_data['after'] = string[index + index2 + 2:-1].strip()
                        break
            elif string[0] in '{':
                separated_data['regular'] = 1  # 用于判断（响应断言）是不是正则表达式，1代表是正则表达式

        return separated_data

    # （URL编码）互转
    def url_coding_conversion(self, string, mode=True):
        """
        将字符串转换为URL编码， 用于URL数据传输
        :param string: 字符串
        :param mode: （True字符转编码）、（False编码转字符）
        :return:
        """
        # 字符转编码
        if mode:
            original_string = string
            encoded_string = urllib.parse.quote(original_string)  # 转换为URL编码格式
            return encoded_string  # 返回编码
        # 编码转字符
        else:
            data = urllib.parse.unquote(string)
            return data

    # （gb2312编码）互转
    def gb2312_code_conversion(self, string, mode=True):
        """
        gb2312编码与解码
        :param string: 需要编码或解码的字符串
        :param mode: 转换模式（True编码），（False解码），默认编码格式
        :return:
        """
        # 编码
        if mode:
            gb2312_bytes = string.encode('gb2312')
            quoted_string = urllib.parse.quote(gb2312_bytes)
            return quoted_string
        # 解码
        else:
            decoded_url = urllib.parse.unquote(string, 'gbk')
            return decoded_url

    # 特殊格式数据提取
    def special_format_data_extract(self, data_):
        """
        用于将[]=[]这种格式数据区分开
        :param data_: []=[]格式字符串
        :return: 返回是一个字典：front前、after后
        """
        string = data_.strip()  # 去除前后空格
        string = Base().symbol_conversion(string)  # 将中文符号转英文符号
        separated_data = {}  # 用于存储区分开后的数据

        # 循环（断言数据）中每个字符与其下标
        for index, value in enumerate(string[:-1]):
            # 如果字符中查询到']'括号，且后面第一个字符为（判断符号），则说明是最后一个列表括号
            if value in [']'] and (string[index + 1]) in ['=']:

                # 【前面部分】：获取前面部分
                separated_data['front'] = (string[1:index]).strip()  # 获取（判断符号）前面部分，并去除其[]括号

                # 再次循环后面部分的
                for index2, value2 in enumerate(string[index + 1:]):
                    # 如果寻找到'['符号，则说明是（后面部分）的数据
                    if value2 in ['[']:
                        # 获取判断符号（后面部分）。并去除其[]括号
                        separated_data['after'] = string[index + index2 + 2:-1].strip()
                        break
        return separated_data

    # 分隔字符串
    def divide_str(self, string, separator, num=-1):
        """
        将字符串用指定的分隔符分开
        :param string: 分隔字符串主体
        :param separator: 分隔符
        :param num: 分隔次数，默认无数次
        :return: 以列表格式返回
        """
        str_ = str(string).split(separator, num)
        return str_

    # 判断文件是否为空
    def null_file_judgment(self, file_path):
        """
        通过文件大小来判断，支持任意种类文件判断
        :param file_path: 文件路径
        :return:
        """
        # 判断文件大小是否为 0
        if os.path.getsize(file_path) == 0:
            return False
        else:
            return True

    # 大小写字母转换
    def transform_case(self, text, upper=True):
        """
        将字符串转换成大写或小写，根据upper参数来控制大小写
        :param text: 传入的字符串
        :param upper: 是否转换成大写，默认为True
        :return: 转换后的字符串
        """
        if not isinstance(text, str):
            raise TypeError("输入的text参数必须是字符串类型")
        if upper:
            return text.upper()
        else:
            return text.lower()

    # 等待
    def wait_time(self, seconds):
        """
        :param seconds: 单位，秒
        :return:
        """
        time.sleep(int(seconds))  # 等待seconds秒
