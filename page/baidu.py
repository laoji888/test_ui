from selenium import webdriver
from common.base import base
from time import sleep


class Baidu(base):

    def element(self, rows):
        """
        获取元素信息
        :param rows: 元素信息所在的行（索引）
        :return:
        """
        element = self.element_info("elements/csms_elements.xlsx", 2, rows, clos=1, ty=1)
        return element

    def baidu(self,v):
        self.send_keys(v,*self.element(0))
        sleep(2)
        self.find_element_click(*self.element(1))
