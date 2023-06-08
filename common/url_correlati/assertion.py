# -*- coding:utf-8 -*-
# @time :2023-5-14 23:54
# @Author :lemon_huahua
# @File: assertion.py
# 文件说明：断言模块
from common.base import Base
from common.edit_file_tool.yaml_tool import YamlOperate


class Assertion:
    # 文件路径定义
    global_path = f'{Base().get_project_path()}/data/config_data/global_variable.yaml'

    # 提取器
    def extractor(self, excel_data, res_data):
        """
        响应提取器：目前仅支持对（响应信息）进行提取，提取语法仅支持（正则表达式）和（json_path语法）
        :param excel_data: excel用例数据
        :param res_data: 接口响应
        :return:
        """
        # 获取excel中（提取器）的内容
        extract_data = excel_data[11]
        # 获取接口响应的（响应信息）
        return_data = res_data[1]  # 获取（响应信息）

        if extract_data and return_data:
            # 用（换行符）将提取器内容分开
            string_l = Base().divide_str(extract_data, '\n')
            for strs in string_l:
                eng_str = Base().symbol_conversion(strs)  # 将中文符号转换为英文
                str_w = Base().divide_str(eng_str, ':', 1)  # 将分隔后的字符，再次用冒号分开，只分隔一次
                colon_front = str_w[0]  # 提取出冒号的前面部分
                colon_after = str_w[1]  # 提取出冒号的后面部分

                dict_info = Base().assertion_type_estimate(colon_after)  # 分隔成前、中、后三部分。是一个字典

                noe_list = dict_info['front']  # 提取（提取器）中第一个列表
                two_list = dict_info['after']  # 提取（提取器）中第二个列表

                # 【响应信息】管理
                if colon_front == '响应信息' and noe_list != '':
                    # 如果语法中，是以"$"符号开头，则认为使用的是json_path语法
                    if noe_list[0] == '$':
                        data_ = Base().json_path(return_data, two_list)  # 使用json_path语法从（接口响应）中提取数据
                    else:  # 否则则认为使用的是正则表达式
                        data_ = Base().regular_extractor(return_data, two_list)
                    # 将提取出来的数据更新到（全局配置）文件
                    YamlOperate().updata_yaml(self.global_path, {noe_list:data_})

    # （响应信息）断言
    def response_info_assertion(self, excel_data, res_data):
        """
        响应信息断言，支持（in、==、!=、>、>=、<、<=）7种断言方式
        :param case_data: excel用例数据
        :param res_data: 接口返回信息
        :return: 返回True表示断言成功，False表示断言失败
        """
        excel_assertion_data = excel_data  # 获取（excel断言数据）
        res_text = res_data  # 获取接口返回的（响应信息）
        assertion_list = []  # 用于存储多种断言结果

        # 用（\n）换行符分隔：用于多种不同判断
        excel_assertion_info = excel_assertion_data.split('\n')

        # 如果第一行不是or，则说明是and方式断言
        if excel_assertion_info[0] != 'or':
            start_index = 0  # and方式断言
        else:
            start_index = 1  # or方式断言

        # 循环多种断言：通过start_index下判断，是走and方式还是or方式
        for assertion_group in excel_assertion_info[start_index:]:
            english_assertion_type = Base().symbol_conversion(assertion_group)  # 将中文符号转换为英文

            # 将断言信息分隔成前、中、后三部分。是一个字典
            assertion_info = Base().assertion_type_estimate(english_assertion_type)

            # front前、middle中、after后、regular是否正则
            front = assertion_info['front']  # 前
            middle = assertion_info['middle']  # 中
            after = assertion_info['after']  # 后
            regular = assertion_info['regular']  # regular是否正则，1为正则，0不为正则

            # 【处理（响应信息）前面部分】
            if regular == 0:  # 等于0表示不是正则语法
                # （响应信息、json_path语法、正则表达式）判断
                if front == 'res':  # 如果等于‘res’，则说明当前条件是那接口（响应信息）做判断
                    res_info = res_text
                elif front[0] == '$' and front[1] != '{':  # 如果（前面部分）是$开头，且第二个字符不为{，则说明是jsonpath语法
                    res_info = Base().json_path(res_text, front)
                # 纯数据计算处理：可以根据输入数据进行计算（已经过全局变量替换）
                elif Base().calculate_expression(front) != 'None':
                    res_info = Base().calculate_expression(front)
                else:  # 其它情况不作处理
                    res_info = front
            # 表示是正则语法
            elif regular == 1:
                res_info = Base().regular_extractor(res_text, front)
            # 其余情况不作处理
            else:
                res_info = front

            # 【后面部分】处理
            if Base().calculate_expression(after) != 'None':
                posterior_part_result = Base().calculate_expression(after)
            else:
                posterior_part_result = after

            # 【判断处理】
            # 包含判断
            if middle in ['in', '包含']:
                results = (posterior_part_result in str(res_info))
            # 等于判断
            elif middle in ['==', '等于']:
                results = (str(res_info) == posterior_part_result)
            # 不等于判断
            elif middle in ['!=', '不等于']:
                results = (str(res_info) != posterior_part_result)
            # 大于判断
            elif middle in ['>', '大于']:
                results = (int(res_info) > int(posterior_part_result))
            # 大于等于判断
            elif middle in ['>=', '大于等于']:
                results = (int(res_info) >= int(posterior_part_result))
            # 小于判断
            elif middle in ['<', '小于']:
                results = (int(res_info) < int(posterior_part_result))
            # 小于等于判断: middle in ['<=','小于等于']
            else:
                results = (int(res_info) <= int(posterior_part_result))
            assertion_list.append(results)  # 将断言结果添加到列表中

        # 如果是and断言方式
        if start_index == 0:
            assertion_result = all(assertion_list)  # all：如果列表中全部为True，则返回True，只要有一个为False则返回False
        # 如果是or断言方式
        else:
            assertion_result = any(assertion_list)  # any：如果列表中只要有一个为True则返回True，全部为False时返回False

        return assertion_result

    # (响应码）断言
    def response_code_assertion(self, excel_data, res_data):
        """
        响应码断言
        :param excel_data: excel用例数据
        :param res_data: 接口返回信息
        :return:
        """
        excel_res_code = excel_data  # 获取excel中的（响应码）
        res_code = res_data  # 获取接口返回的（响应码）
        # 如果excel中的（响应码）等于（接口返回响应码），则返回True，否则返回False

        if int(excel_res_code) == int(res_code):
            return True
        else:
            return False

