from selenium import webdriver
from common.ui_base import base
from time import sleep


class Home(base):

    def element(self, rows):
        """
        获取元素信息
        :param rows: 元素信息所在的行（索引）
        :return:
        """
        element = self.element_info("elements/csms_elements.xlsx", 0, rows, clos=1, ty=1)
        return element

    def login(self, name, pwd):
        """
        登录到csms
        :param name: 用户名
        :param pwd: 密码
        :return:
        """
        self.open()
        self.send_keys(name, *self.element(0))
        self.send_keys(pwd, *self.element(1))
        self.find_element_click(*self.element(2))

    def log_in_again(self, name, pwd):
        """
        在登录状态下重新登录
        :param name: 用户名
        :param pwd: 密码
        :return:
        """
        self.action_chains(*self.element(6))
        self.action_chains(*self.element(4))
        self.find_element_click(*self.element(5))
        self.send_keys(name, *self.element(0))
        self.send_keys(pwd, *self.element(1))
        self.find_element_click(*self.element(2))

    # 进入工作台
    def enter_workbench(self):
        """
        登录后进入工作台
        :return:
        """
        self.find_element_click(*self.element(7))

    def enter_Recruitment_management(self):
        """
        鼠标悬停到合作伙伴管理后点击招募管理
        :return:
        """
        self.action_chains(*self.element(8))
        self.find_element_click(*self.element(9))
        sleep(2)
        self.action_chains(*self.element(10))
        self.find_element_click(*self.element(10))
