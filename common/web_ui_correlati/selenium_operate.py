# -*- coding:utf-8 -*-
# @time :2023-6-4 16:02
# @Author :lemon_huahua
# @File: selenium_operate.py
# 文件说明：selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.base import Base


class SeleniumTool:
    # 创建一个浏览器实例
    wd = webdriver.Chrome()

    # 打开浏览器
    def open_browser(self, url_):
        """
        打开浏览器， 支持指定驱动路径
        :param url_: 需要打开的网址
        :return:
        """
        self.wd.maximize_window()  # 最大化浏览器
        self.wd.get(url_)  # 打开地址

    # 获取元素信息
    def locator(self, **key_ward):
        """
        :param args: args[0]定位方式、args[1]元素信息
        :return: 元素定位的值
        """
        xp = key_ward['loc_mode']  # 获取元素定位方法
        ele = key_ward['ele_info']  # 获取元素信息
        loc_mode = Base().transform_case(xp)  # 将定位方式全部转为大写

        # 寻找元素10秒， 每0.5秒寻找一次，如果寻找不到则会抛异常
        wait = WebDriverWait(self.wd, 10)
        element = wait.until(EC.presence_of_element_located((getattr(By, loc_mode), ele)))
        return element

    # 输入
    def input_data(self, txt, **key_ward):
        """
        :param txt: 输入值
        :param ele: 元素信息
        :param xp: 元素定位方式
        :return:
        """
        loc = self.locator(**key_ward)  # 获取元素信息
        loc.clear()  # 清空输入框
        loc.send_keys(txt)  # 输入内容

    # 点击
    def click_ele(self, **key_ward):
        loc = self.locator(**key_ward)  # 获取元素信息
        loc.click()  # 点击元素

    # 关闭浏览器
    def shut_browser(self):
        self.wd.quit()




# 打开浏览器
SeleniumTool().open_browser('http://114.55.177.127/index.php/home')
# 点击弹窗
SeleniumTool().click_ele(loc_mode='xpath', ele_info='//div[@class="close-fixed-suspension"]')
# 点击（登录）按钮,打开登录界面
SeleniumTool().click_ele(loc_mode='xpath', ele_info='//a[text()="请登录"]')
# 输入用户名
SeleniumTool().input_data(loc_mode='xpath', ele_info='//input[@placeholder="用户名/手机号"]', txt='user123')
# 输入密码
SeleniumTool().input_data(loc_mode='xpath', ele_info='//input[@placeholder="密码"]', txt='user123')
# 点击登录按钮，登录系统
SeleniumTool().click_ele(loc_mode='xpath', ele_info='//input[@value="登录"]')
# 等待5秒
Base().wait_time(5)
# 关闭浏览器
SeleniumTool().shut_browser()