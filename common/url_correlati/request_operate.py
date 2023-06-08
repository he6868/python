# -*- coding:utf-8 -*-
# @time :2023-5-10 22:25
# @Author :lemon_huahua
# @File: request_operate.py
# 文件说明：request请求操作
import json
import time
import requests
from common.base import Base
from urllib.parse import parse_qs
from common.logger_operate import Logger
from common.edit_file_tool.yaml_tool import YamlOperate


class Request:
    sess = requests.session()

    def __init__(self):
        # 【文件路径定义】
        self.global_path = f'{Base().get_project_path()}/data/config_data/global_variable.yaml'  # 全局变量文件
        self.config_path = f'{Base().get_project_path()}/data/config_data/config_data.yaml'  # 配置文件
        self.cookies_path = f'{Base().get_project_path()}/data/config_data/session.txt'  # cookies文件

    # 请求方式处理
    def req_mode_deal_with(self, case_data):
        # 提取（请求方式），并转换为小写
        req_mode = case_data[6].lower()
        return req_mode

    # URL处理
    def url_deal_with(self, case_data):
        # 如果报错， 则说明主机IP写得是实际IP，否则则说明通过配置文件获取IP
        try:
            int(case_data[7])
        except ValueError:
            ip_ = f'{case_data[7]}{case_data[8]}'
        else:
            # 读取yaml文件
            yaml_datas = YamlOperate().read_yaml(self.config_path)
            url_ = yaml_datas['URL']

            # 通过下标读取主机IP
            ip_ = url_[int(case_data[7])]
        # 返回接口：IP+路径
        return f'{ip_}'

    # 请求头处理
    def head_deal_with(self, case_data):
        head_datas = case_data[9]
        # 将excel里面的请求用换行符分隔开来
        heads = head_datas.split('\n')
        # 用于存储请求头
        head_dicts = {}
        for head in heads:  # 遍历循环分隔后的数据
            subscript = head.find(':')  # 获取第一个冒号的下标

            # 将冒号的前面部分作为key，将冒号后面部分作为value
            head_dicts[str(head[:subscript]).strip()] = str(head[subscript + 1:]).strip()

        # 返回字典格式请求头，方便后续执行
        return head_dicts

    # 请求体处理
    def body_deal_with(self, case_data):
        body_data = case_data[10]  # 定义请求体
        heads = self.head_deal_with(case_data)  # 获取请求头的（Content-Type），用于判断请求体的数据类型
        data_ = None
        if body_data:  # 如果请求体不为空
            # 获取请求的：Content-Type，判断是（json、表单、html）数据格式
            if 'application/json' in heads['Content-Type']:
                data_ = json.loads(body_data)
            # 当请求体是表单数据格式
            elif 'application/x-www-form-urlencoded' in heads['Content-Type']:
                data_ = parse_qs(body_data)
        return data_

    # 发送请求
    def all_request(self, case_data):
        mode = self.req_mode_deal_with(case_data)  # （请求方式）处理
        url = self.url_deal_with(case_data)  # （请求URL）处理
        head = self.head_deal_with(case_data)  # （请求头）处理
        body = self.body_deal_with(case_data)  # （请求体）处理

        start_time = time.time()  # 获取接口开始时间

        # 发送请求
        res = getattr(self.sess, mode)(
            url=url,
            data=body,
            headers=head,
            files=None
        )

        # 【统计接口耗时处理】
        time_ = time.time() - start_time  # 计算时间差

        # 【日志处理】
        Logger().test_case_log(case_data, mode, url, head, body, [res.status_code, res.text])

        # 返回（状态码）、（响应文本）、（接口耗时）
        return res.status_code, res.text, time_
