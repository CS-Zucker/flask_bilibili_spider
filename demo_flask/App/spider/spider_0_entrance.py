from .fake_useragent import useragent_random

from .spider_1_video import spider_video_data
from .spider_2_stopword import BiliSpider



def spider_entrance(bv: str):
    headers = useragent_random()

    word_spider = BiliSpider(headers, bv)
    msg = word_spider.run()    

    if msg[:7] == "[WORK!]":     
        spider_video_data(headers, bv)
        return msg
    else:
        return msg

if __name__ == "__main__":
    # spider_entrance(input("url: "))  
    res=spider_entrance(r"BV1T94y1e74E")  
    print(res)
    # spider_entrance(r"【它真的来了! [中文字幕]《蜘蛛侠:逝去之莲》饭制电影丨Spider-Man Lotus】 https://www.bilibili.com/video/BV1G94y1k7Wy/?share_source=copy_web&vd_source=01fe51be663826229447bea0d10f5b7b")  
