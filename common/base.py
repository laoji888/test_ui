import datetime

import pymysql
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import xlrd
from selenium import webdriver
from common.log import log
from selenium.webdriver.common.by import By


# 封装selenium常用方法
class base():

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.transfer_code = '123'
        self.log = log().ll(logs_path="./logs/ui_log.log")
        now_time = datetime.datetime.now()  # 获取时间
        self.t1 = (now_time + datetime.timedelta(seconds=+60)).strftime("%Y-%m-%d %H:%M:%S")  # 当前时间+60
        self.t2 = (now_time + datetime.timedelta(seconds=+120)).strftime("%Y-%m-%d %H:%M:%S")  # 当前时间+120

    def open(self):
        """
        判断browser类型并打开对应的浏览器，最大化
        :return:
        """
        self.driver.get(self.url)
        sleep(1)
        self.driver.maximize_window()

    def driver_quit(self):
        self.driver.quit()

    def add_style(self, *loc):
        """
        给操作元素添加样式（红框）
        :param loc: 元素信息，格式是元祖
        :return:
        """
        try:
            ele = self.driver.find_element(*loc)
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",
                                       ele, "border: 2px solid red;")
        except:
            pass

    def set_style(self, *loc):
        """
        操作元素后把红框改成蓝框
        :param loc:
        :return:
        """
        try:
            ele = self.driver.find_element(*loc)
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",
                                       ele, "border: 2px solid blue;")
        except:
            pass

    def wait(self):
        """
        等待页面元素加载完毕，如果20秒后没有加载完成执行一次刷新
        :return:
        """
        try:
            self.driver.implicitly_wait(20)
        except:
            self.driver.refresh()

    def find_element_click(self, *loc):
        """
        定位到元素并点击,如果点击失败尝试等待两面再次点击，再次点击失败后写入日志。
        :param loc: 元素信息，格式为元祖
        """

        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(loc))
        sleep(0.5)
        self.add_style(*loc)

        try:
            self.driver.find_element(*loc).click()
        except Exception as e:
            self.log.error("元素点击失败{}".format(e))

        self.set_style(*loc)

    def find_element(self, *loc):
        """
        定位元素，返回对象
        :param loc: 元素信息
        :return: 返回元素的对象
        """
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(loc))
        self.add_style(*loc)

        try:
            ele = self.driver.find_element(*loc)
            return ele
        except Exception as e:
            self.log.error("元素错误{}".format(e))
            pass

    def find_elements(self, index, *loc):
        """
        定位元素集合，用索引，点击
        :param index: 元素索引
        :param loc: 元素信息（元祖）
        """
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(loc))
        self.add_style(*loc)
        try:
            self.driver.find_elements(*loc)[index].click()
            self.set_style(*loc)
        except Exception as e:
            self.log.error(e)
            pass

    # 下拉类表选择
    def select(self, index, *loc):
        """
        select操作下拉框
        :param index:元素索引
        :param loc: 元素信息（元祖）
        """
        self.add_style(*loc)
        ele = self.driver.find_element(*loc)
        Select(ele).select_by_index(index)

    def js(self, ele):
        """
        执行js代码
        :param ele:
        :return:
        """
        self.driver.execute_script(ele)

    def send_keys(self, value, *loc):
        """
        定位元素后清空并输入数据
        :param value: 输入的数据
        :param loc: 元素信息
        """
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(loc))
        self.add_style(*loc)
        self.driver.find_element(*loc).send_keys(Keys.CONTROL + "a")
        self.driver.find_element(*loc).send_keys(Keys.BACKSPACE)

        try:
            self.driver.find_element(*loc).send_keys(value)
            self.set_style(*loc)
        except Exception as e:
            self.log.error(e)
            pass

    # 切换frame
    def switch_to_frame(self, *frame_id):
        """
        切换frame框架
        :param frame_id: frame框架元素信息（元祖）
        """
        ele = self.driver.find_element(*frame_id)
        self.driver.switch_to.frame(ele)

    def action_chains(self, *loc):
        """
        鼠标悬停一次,操作完成后有两秒的等待时间
        :param loc: 元素信息（元祖）
        """
        ele = self.driver.find_element(*loc)
        self.add_style(*loc)
        ActionChains(self.driver).move_to_element(ele).perform()
        self.set_style(*loc)
        sleep(2)

    def action_chains_2(self, *loc):
        """
        鼠标连续悬停
        :param loc:
        """
        a = ActionChains(self.driver)
        a.move_to_element(*loc)
        a.pause(1)
        a.move_to_element(*loc)
        a.pause(1)
        a.perform()

    def element_info(self, element_path, sheet_index, rows, clos=1, ty=1):
        """
        读取xlsx,ty=1是返回元祖，ty=2时先转换成整形在转换成字符串，ty=3时转换成字符串
        :param sheet_index: sheet页
        :param rows: 行
        :param clos: 列
        :param ty: 返回的数据类型
        :return:
        """
        page = xlrd.open_workbook(element_path)  # 打开文件
        table = page.sheet_by_index(sheet_index)  # 获取sheet页
        e = table.cell_value(rows, clos)

        if ty == 1:
            ele = tuple(eval(e))
            return ele
        elif ty == 2:
            x = int(e)
            y = str(x)
            return y
        elif ty == 3:
            z = str(e)
            return z

    def is_display(self, *loc):
        """
        判断元素是够显示，显示返回True，不显示返回False
        :param loc:
        :return:
        """

        try:
            self.driver.find_element(*loc).is_displayed()
            return True
        except:
            return False

    def switch_to_window(self, num=0):
        """切换至某一页面(句柄)
        Agrs:
         - num - 选择页面
         第一个页面的num值为0
         #默认切换至第一页
        Usage:
         self.switch_to_window(1)
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[num])
        self.log.info('跳转浏览器页面')

    def link_sql(self, selector, sentence):
        """调取数据库及查询
        Agrs:
        - host - 数据库地址
        - user - 数据库登录用户名称
        - pw - 数据库登录用户密码
        - db - 数据库中库的名称
        - charset - 数据库中库的字符集
        - sentence - 对数据的select语句
        Usage:
         self.link_sql(self.["localhost", "root", "password", "world2", "utf8"], "SELECT title FROM article where id =1")
        """
        try:
            host = selector[0]
            user = selector[1]
            pw = selector[2]
            db = selector[3]
            charset = selector[4]
            db = pymysql.connect(host=host,
                                 port=3306,
                                 user=user,
                                 passwd=pw,
                                 db=db,
                                 charset=charset)
            self.log.info('已链接数据库')
        except Exception:
            raise Exception(self.log.error('链接数据库内容出错'))
        else:
            cursor = db.cursor(pymysql.cursors.DictCursor)  # cursor() 方法获取操作游标
            sql = sentence
            cursor.execute(sql)  # 执行SQL语句
            self.log.info('执行SQL语句')
            results = cursor.fetchall()  # 获取所有记录列表
            self.log.info('返回查询结果，请赋值')
            return results


if __name__ == '__main__':
    driver = webdriver.Firefox()
    aa = (By.ID, 'kw1')
    dr = base(driver,"https://www.baidu.com")
    sleep(2)
    dr.find_element(*aa)
    sleep(5)
    dr.driver_quit()
