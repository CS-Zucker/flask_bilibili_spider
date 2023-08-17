import re
from lxml import etree
import requests

from .fake_useragent import useragent_random
from .spider_data.database import Database


def spider_video_data(headers, bv: str) -> dict:
    video_data = {}
    url = f"https://www.bilibili.com/video/{bv}"

    with requests.get(url, headers=headers, timeout=10) as rep:
        html = etree.HTML(rep.text)
        if rep.status_code == 200:
            title_text = html.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/h1/text()')[0]
            up_text = html.xpath(
                '//*[@id="app"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/a/@href')[0]
            pub_time_text = html.xpath('/html/head/meta[17]/@content')[0]

            if bv:
                video_data["video_bv_num"] = bv
            if title_text:
                video_data["video_name"] = title_text
            if up_text:
                video_data["video_up_uid"] = re.findall(r'\d+', up_text)[0]
            if pub_time_text:
                video_data["video_pub_time"] = pub_time_text
                
            video_data_todb(video_data)
        else:
            error_msg = "获取失败"
            print(error_msg)


def video_data_todb(video_data):
    video_db = Database(host="127.0.0.1", username="root",
                        password="1234", db_name="bilibili")
    video_db_select = video_db.execute_sql(table_name="video", mode="search",
                                      key="video_bv_num", value=video_data["video_bv_num"])
    if video_db_select != 0:
        print('此视频已存在！bv:{}'.format(video_data['video_bv_num']))
        print('-' * 60)
    else:
        video_db.execute_sql(table_name="video", mode="insert",
                              keys=list(video_data.keys()), values=list(video_data.values()))
        print('此视频信息插入成功！')
        print('-' * 60)



if __name__ == "__main__":
    headers = useragent_random() 
    spider_video_data(headers, r"BV1G94y1k7Wy")

    # spider_video_data(headers, r"url:【它真的来了! [中文字幕]《蜘蛛侠:逝去之莲》饭制电影丨Spider-Man Lotus】 https://www.bilibili.com/video/BV1G94y1k7Wy/?share_source=copy_web&vd_source=01fe51be663826229447bea0d10f5b7b")

