# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
import json
from scrapy.http import HtmlResponse
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaobaoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # 对象初始化
    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url
        self.wb_username = '***'
        self.wb_password = '***'
        options = webdriver.ChromeOptions()
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_argument('--log-level=3')
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s
        self.keyword = '美食'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if request.url == 'https://login.taobao.com/member/login.jhtml':
            self.browser.get(self.url)
            # 点击账号登录
            password_login = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
            password_login.click()
            # 通过微博账号登录
            weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
            weibo_login.click()
            # 输入账号
            weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
            weibo_user.send_keys(self.wb_username)
            # 输入密码
            weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
            weibo_pwd.send_keys(self.wb_password)
            # 点击登录
            submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
            submit.click()
            time.sleep(2)
            # 在搜索栏中输入关键词并点击搜索
            search = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="search-combobox-input-wrap"]/input[@id="q"]')))
            search.send_keys(self.keyword)
            time.sleep(1)
            search_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="search-button"]/button')))
            search_button.click()
            time.sleep(1)
            # 将渲染后的网页源码作为返回对象的body，构造一个response对象传给spider
            body = self.browser.page_source
            response = HtmlResponse(url=request.url, body=body, encoding='utf-8')
            return response



    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
