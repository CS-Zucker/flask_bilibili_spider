# coding=utf-8
import requests
import pandas as pd
from lxml import etree
import re
import time
import pymysql

from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()

from .fake_useragent import useragent_random
from .spider_data.database import Database


class BiliSpider:
    def __init__(self, headers, BV):
        # 构造要爬取的视频url地址
        self.BV = BV
        self.BVurl = "https://m.bilibili.com/video/"+BV
        self.headers = headers
        self.info_table = pd.DataFrame(columns=['弹幕'])
        self.row_cnt = 1

    # 弹幕都是在一个url请求中，该url请求在视频url的js脚本中构造
    def getXml_url(self):
        # 获取该视频网页的内容
        response = requests.get(self.BVurl, headers = self.headers)
        html_str = response.content.decode()

        # 使用正则找出该弹幕地址
        # 格式为：https://comment.bilibili.com/168087953.xml
        # 我们分隔出的是地址中的弹幕文件名，即 168087953
        getWord_url = re.findall('"cid":(\d{6,10})', html_str)
        getWord_url = getWord_url[0]
        # 组装成要请求的xml地址
        xml_url = "https://comment.bilibili.com/{}.xml".format(getWord_url)
        return xml_url

    # Xpath不能解析指明编码格式的字符串，所以此处我们不解码，还是二进制文本
    def parse_url(self,url):
        response = requests.get(url,headers = self.headers)
        return response.content

    # 弹幕包含在xml中的<d></d>中，取出即可
    def get_word_list(self,str):
        html = etree.HTML(str)
        word_list = html.xpath("//d/text()")
        return word_list

    def run(self):
        # 1.根据BV号获取弹幕的地址
        start_url = self.getXml_url()
        # 2.请求并解析数据
        xml_str = self.parse_url(start_url)
        word_list = self.get_word_list(xml_str)       
        # 3.存储弹幕 (弹幕信息过少->不存储)
        if len(word_list)>10:
            for word in word_list:
                # print(word)
                alist = []
                alist.append(word)
                self.info_table.loc[self.row_cnt] = alist
                self.row_cnt += 1
            try:
                DB_STRING = 'mysql+mysqldb://root:1234@127.0.0.1:10306/stopword'
                engine = create_engine(DB_STRING) 
                self.info_table.to_sql(self.BV,con=engine,chunksize=1000,if_exists='replace',index=False)
                print("[DATABASE]: stopword, [TABLE]: "+self.BV+", 弹幕数据库存储成功...")
                print('-' * 60)
                do_msg = "[WORK!]：弹幕信息录入成功"
                return do_msg
            except Exception as e:
                print("[ERROR]：", e)
                print('-' * 60)
        else:
            error_msg = "[ERROR]: 弹幕信息可能过少，无法绘制词云图"
            return error_msg   


if __name__ == '__main__':
    headers = useragent_random() 
    spider = BiliSpider(headers, "BV1T94y1e74E")
    spider.run()
