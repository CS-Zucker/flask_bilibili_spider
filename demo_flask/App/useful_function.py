import pymysql
import re
import jieba.analyse

from spider.spider_data.database import Database

def get_bv(url: str) -> str:
    bv_number_pattern = r'(BV[0-9a-zA-Z]*)'
    bv = re.findall(bv_number_pattern, url) 
    if bv:
        bv = bv[0]
        return bv
    else:
        error_msg = "[ERROR]: 链接可能不正确，无法匹配到bv号"
        return error_msg   


# 连接bilibili数据库并提取视频信息
def get_video_info(bv):
    video_db = Database(host="127.0.0.1", username="root",
                        password="1234", db_name="bilibili")
    bv_select_list = video_db.execute_sql(table_name="video", mode="search",
                                      key="video_bv_num", value=bv, data_type="all_list")
    video_url = f"https://www.bilibili.com/video/{bv}"
    up_url = f"https://space.bilibili.com/{bv_select_list[2]}"
    bv_select_list.append(video_url)
    bv_select_list.append(up_url)
    return bv_select_list



# 连接stopword数据库并提取文字（词）内容
def get_word_data_list(bv):
    word_db = Database(host="127.0.0.1", username="root",
                        password="1234", db_name="stopword")
    #准备词云所需的文字（词）
    db_select_tuple = word_db.execute_sql(table_name=bv, mode="search",
                                      key="弹幕", data_type="all_list")
    word_datalist = [word_tuple[0] for word_tuple in db_select_tuple]
    return word_datalist


# 对数据库文本内容进行分词，并返回 data_inf0 = [弹幕数，词汇数] ->word.html展示的内容
def get_word_data_list_info(word_datalist):
    # 取出数据库中的新闻内容，进行分词
    text = " "
    for item in word_datalist:
        text =  text + item
    cut = jieba.cut(text)
    cut = [word for word in cut if len(word)>1]
    string = ' '.join(cut)
    
    data_info = [len(word_datalist), len(cut)]
    return data_info,string


# 对输入文本进行分词，并返回词汇权重
def get_word_weights(string, topK):
    words = []
    weights = []
    for x, w in jieba.analyse.textrank(string, withWeight=True, topK=topK):
        words.append(x)
        weights.append(w)
    return words,weights


# 文本关键字提取
def get_keyword_from_content(content):
    print(content)
    cut = jieba.cut(content)
    string = ' '.join(cut)
    words,_=get_word_weights(string, topK=5)
    return words.append('（自动生成）')