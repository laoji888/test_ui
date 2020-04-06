import os
import time
import unittest

from BeautifulReport import BeautifulReport
from selenium.webdriver import DesiredCapabilities
from common.base import base
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from BeautifulReport import BeautifulReport
from common.base import base
import unittest
from page.baidu import  Baidu


class asw(unittest.TestCase):
    def save_img(self, img_name):  # 错误截图方法
        """
        传入一个img_name, 并存储到默认的文件路径下
        :param img_name:
        :return:
        """
        self.driver.get_screenshot_as_file('{}/{}.png'.format(os.path.abspath(
            r"img"),
            img_name))  # os.path.abspath(r"G:\Test_Project\img")截图存放路径

    def setUp(self):
        a = 10


    @BeautifulReport.add_test_img("test_a")
    def test_a(self):
        self.driver = webdriver.Remote(command_executor="106.13.132.197:8888/wd/hub",
                                       desired_capabilities=DesiredCapabilities.FIREFOX)
        self.dr = Baidu(self.driver,"https://www.baidu.com")
        self.dr.open()
        self.dr.baidu("java")


    def tearDown(self):
        self.dr.driver_quit()



