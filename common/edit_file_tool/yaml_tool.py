# -*- coding:utf-8 -*-
# @time :2023-5-10 23:21
# @Author :lemon_huahua
# @File: yaml_tool.py
# 文件说明：yaml文件操作
import yaml


class YamlOperate:

    # 读取yaml文件
    def read_yaml(self, path):
        # 打开文件： yaml文件路径、r读取、编码、 重命名为文件流
        with open(path, 'r', encoding='utf-8') as f:
            # 加载文件： 文件流、加载方式
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
            return data

    # 更新yaml文件内容，具体方法为（提取>修改>写入）
    def updata_yaml(self, path, dict_key, mode='w'):
        """
        :param path: 修改yaml文件路径
        :param dict_key: 字典
        :param mode: 写入模式，默认为w覆盖，a追加
        :return:
        """
        # 读取yaml文件
        old_data = self.read_yaml(path)
        if old_data is None:
            old_data = {}

        # 遍历字典， 循环写入
        for key, value in dict_key.items():
            # 修改读取的数据（key存在就修改对应值，key不存在就新增一组键值对）
            old_data[key] = value
            # 将修改后的字典写入yaml
            with open(path, mode, encoding="utf-8") as f:
                yaml.dump(old_data, f, allow_unicode=True)


# YamlOperate().updata_yaml(r'C:\Users\86158\Desktop\pythonProject3\data\config_data\global_variable.yaml', {'cookie': {'a':'a'}})
