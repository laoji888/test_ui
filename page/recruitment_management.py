

from selenium import webdriver
from common.base import base
from time import sleep


class Recruitment_management(base):

    # 获取元素信息
    def element(self, rows):
        element = self.element_info("elements/csms_elements.xlsx", 1, rows, clos=1, ty=1)
        return element

    # 申请招募
    def apply_recruitment(self,v1,v2):
        """
        合作管理员申请招募
        :param v1: 招募名称
        :param v2: 招募内容
        :return:
        """
        self.find_element_click(*self.element(0))
        sleep(2)
        self.send_keys(v1,*self.element(1))
        self.switch_to_frame(*self.element(2))
        self.switch_to_frame(*self.element(3))
        self.send_keys(v2,*self.element(4))
        self.driver.switch_to.default_content()
        self.send_keys(self.t1,*self.element(5))
        self.send_keys(self.t2,*self.element(6))
        self.find_element_click(*self.element(7))
        sleep(1)
        self.find_element_click(*self.element(8))
        self.find_element_click(*self.element(9))
        sleep(1)
        self.find_element_click(*self.element(10))
        sleep(1)
        self.find_element_click(*self.element(11))
        self.find_element_click(*self.element(12))

    # 进入工作台下的合作伙伴管理（一二级审批使用）
    def partner_management(self,value):
        """
        判断后进行一级二级审批
        :param value: 审批意见
        :return:
        """
        self.find_element_click(*self.element(14))
        sleep(2)
        self.send_keys(value,*self.element(15))
        self.find_element_click(*self.element(16))
        sleep(1)
        self.find_element_click(*self.element(17))

        sleep(1)
        button = self.is_display(*self.element(18))
        if button:
            self.find_element_click(*self.element(18))
            self.find_element_click(*self.element(19))
        else:
            pass

        self.send_keys(value, *self.element(20))
        self.find_element_click(*self.element(21))
        self.find_element_click(*self.element(22))






