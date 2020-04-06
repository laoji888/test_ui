import warnings

from selenium.webdriver import DesiredCapabilities
from page.home import Home
from page.recruitment_management import Recruitment_management
import time, unittest
from selenium import webdriver
from time import sleep


class CsmsTest(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Firefox()
        warnings.simplefilter("ignore", ResourceWarning)

        # 调用指定的执行机
        self.driver = webdriver.Remote(command_executor='192.168.31.152:1112/wd/hub',
                                       desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)

        # 调用集群浏览器，docker自动分配执行机
        self.driver = webdriver.Remote(command_executor='http://106.13.132.197:8888/wd/hub',
                                       desired_capabilities={'browserName': 'firefox',
                                                             # "version": "",
                                                             # "platform": "",
                                                             # "javascriptEnabled": True,
                                                             # "marionette": True,
                                                             }
                                       )
        self.url = "http://120.52.157.131:58080/#/home/cooperation"
        self.home = Home(self.driver, self.url)
        self.rm = Recruitment_management(self.driver, self.url)

    def test_login(self):
        # 乔琳登录
        self.home.login("qiaolin", "ChinaTower1234")
        time.sleep(1)
        v1 = self.home.find_element(*self.home.element(3))
        self.assertIn("乔琳", v1.text, msg='错误')

        # 进入合作伙伴管理下的招募管理
        self.home.enter_workbench()
        sleep(5)
        self.home.enter_Recruitment_management()
        time.sleep(1)

        # 申请招募
        self.rm.apply_recruitment("自动化测试0808", "测试")
        v2 = self.rm.find_element(*self.rm.element(13))
        self.assertIn("成功", v2.text, msg='错误')
        sleep(3)

        # 退出登录后一级审批登录
        self.home.log_in_again("yjsp", "ChinaTower1234")
        v3 = self.home.find_element(*self.home.element(3))
        self.assertIn("一级审批", v3.text, msg='错误')

        # 一级审批审批合
        self.home.enter_workbench()
        sleep(5)
        self.rm.partner_management("自动化测试0808")
        sleep(2)

        # 退出登录后二级审批登录
        self.home.log_in_again("ejshp", "ChinaTower1234")
        v3 = self.home.find_element(*self.home.element(3))
        self.assertIn("二级审批", v3.text, msg='错误')

        # 二级审批审批
        self.home.enter_workbench()
        sleep(5)
        self.rm.partner_management("自动化测试0808")
        v4 = self.rm.find_element(*self.rm.element(13))
        self.assertIn("成功", v4.text, msg='错误')
        sleep(3)

    def tearDown(self):
        self.driver.quit()
