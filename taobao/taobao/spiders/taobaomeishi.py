# -*- coding: utf-8 -*-
import scrapy
import re
import json
from ..items import TaobaoItem
from urllib.parse import urlencode


class TaobaomeishiSpider(scrapy.Spider):
    name = 'taobaomeishi'
    allowed_domains = ['taobao.com']
    start_urls = ['https://login.taobao.com/member/login.jhtml']

    def parse(self, response):
        item = TaobaoItem()
        # 得到渲染后的网页源码后， 用正则匹配出所需json格式的数据
        data = re.findall(r'g_page_config = (.*?)g_srp_loadCss', response.body.decode(), re.S)
        str_data = data[0].strip()[:-1]
        json_data = json.loads(str_data)
        for each_item in json_data.get('mods').get('itemlist').get('data').get('auctions'):
            item['raw_title'] = each_item['raw_title']
            item['pic_url'] = each_item['pic_url']
            item['detail_url'] = each_item['detail_url']
            item['price'] = each_item['view_price']
            item['loc'] = each_item['item_loc']
            item['sales'] = each_item['view_sales']
            item['shop'] = each_item['nick']
            yield item
        basic_url = 'https://s.taobao.com/search?'
        # 手动复制cookies，若不带cookie访问则得不到数据
        cookies = 'cna=qrQYFFCoF28CARt6GX7X6wZv; t=9ff4f848ac50f3acff997f0be6f1ef69; thw=cn; tg=0; enc=lqxGRcZ2j2%2BiUw7rnqe2rg53Qj1ib0eV9s67ejtTO3GZJ%2FNHNWV149q80%2FywOF8knUu0Zj21NPxPTjczkWKAsg%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; miid=920557281192675460; _m_h5_tk=c956f9dd6707bb3ed68d7a70964f674a_1558172655396; _m_h5_tk_enc=4b62e5134e3d2457c1172d1e7965963e; cookie2=19d023bae37d6d1a035a8969ebfd221f; _tb_token_=ee17f7b318e6e; v=0; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=6AE93F0E64EBE39F24A4CF970AE4846C; unb=2286448769; uc1=cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=UtASsssme%2BBq&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTZ7HcsubA8eg%3D%3D&tag=8&lng=zh_CN; sg=096; _l_g_=Ug%3D%3D; skt=b1a790d3d8815f84; cookie1=W8gytojtKutZGtBUI8E4M82RMlgEOf27P1TQ36J8JAQ%3D; csg=c6dc1ac5; uc3=vt3=F8dBy3qDGyWfud0iah8%3D&id2=UUpprnHVuBo9Qg%3D%3D&nk2=DkJtVtDlxelbMA%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; existShop=MTU1ODI3NDE4MQ%3D%3D; tracknick=mr%5Cu5218%5Cu5148%5Cu751F10; lgc=mr%5Cu5218%5Cu5148%5Cu751F10; _cc_=URm48syIZQ%3D%3D; dnk=mr%5Cu5218%5Cu5148%5Cu751F10; _nk_=mr%5Cu5218%5Cu5148%5Cu751F10; cookie17=UUpprnHVuBo9Qg%3D%3D; mt=ci=0_0&np=; l=bBQ6Veyev_7Mo-jABOfaquI8aob9FFRX1PVzw4_GqIB19f6KDp3P4HwdRnMW63Q_E_5KahKzPtLPWRFkWDU38x1..; isg=BGBgzhb1KEL60ZMwFM-C0PSjMW7ywURX7qh9oNptjnOJ1Q__l3uswnyjbT1w4PwL'
        cookies = dict(i.split('=',1) for i in cookies.split(';'))
        for i in range(1,100):
            query_data = {'data-key' : 's',
                'data-value' : 44*i,
                'ajax' : 'true',
                'q' : '美食',
                'commend' : 'all',
                'ssid' : 's5-e',
                'search_type' : 'item',
                'sourceId' : 'tb.index'
            }
            food_url = basic_url + urlencode(query_data)
            yield scrapy.Request(url=food_url, cookies=cookies,callback=self.parse_food)

    def parse_food(self, response):
        item = TaobaoItem()
        json_data = json.loads(response.body.decode())
        for each_item in json_data.get('mods').get('itemlist').get('data').get('auctions'):
            item['raw_title'] = each_item['raw_title']
            item['pic_url'] = each_item['pic_url']
            item['detail_url'] = each_item['detail_url']
            item['price'] = each_item['view_price']
            item['loc'] = each_item['item_loc']
            item['sales'] = each_item['view_sales']
            item['shop'] = each_item['nick']
            yield item




