from flask import Flask, redirect,render_template, url_for
import pymysql
from model.forms import SearchForm
from flask import request

import useful_function as useful_function

from spider.spider_data.database import Database
from spider.spider_0_entrance import spider_entrance
from spider.spider_1_video import spider_video_data
from spider.spider_2_stopword import BiliSpider
from word_cloud import draw_wordcloud


app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"

# 初始页
@app.route('/')
def home():
    return index()

# 首页重定位
@app.route('/index')
def index():
    return redirect(url_for('search_page'))

# @app.route('/temp')
# def temp_page():
#     return index()


# 搜索界面
@app.route('/search')
def search_page():
    form = SearchForm()
    search_info = ''
    return render_template('search.html', form=form, search_info=search_info)


# 搜索结果返回界面，返回时展示数据库中所有内容，包括正文文本
@app.route('/result_word_analysis',methods=['POST','GET'])
def newsResult_page():
    form = SearchForm()
    search = request.args.get("query")
    
    bv = useful_function.get_bv(search)
    if bv[:7] == "[ERROR]":
        return render_template('search.html', form=form, search_info=bv)

    msg = spider_entrance(bv)
    if msg[:7] == "[ERROR]":
        return render_template('search.html', form=form, search_info=msg)

    # 提取bilibili数据库[video]内容 -> video_info_list
    video_info_list = useful_function.get_video_info(bv)

    # 提取stopword数据库[bv]弹幕内容 -> word_data_list  
    word_data_list = useful_function.get_word_data_list(bv)
   
    # 分析word_data_list弹幕内容，并对文本内容分词生成 -> words_info, string
    words_info_list, string = useful_function.get_word_data_list_info(word_data_list)

    # 计算 topK 的词汇对应的词频
    words,weights = useful_function.get_word_weights(string, topK=16)    

    # 传入 string 进行词云绘图
    draw_wordcloud(bv, string)


    return render_template("result_word_analysis.html",
                            video_info=video_info_list,
                            words_info=words_info_list,
                            words=words, weights=weights, 
                            form=form, BV=bv)



# # 新闻缩略页
# @app.route('/news')
# def news_page():
#     return render_template("news.html",news=datalist)


# # 基于词频绘制的词云
# @app.route('/word')
# def word_page():
#     return render_template("word.html",news_info=data_info)


# 链接到我的个人主页
@app.route('/team')
def team_page():
    return render_template("team.html")


# # 数据库文本信息分析，topK8的词语及频率，暂时用的是直方图
# @app.route('/analysis')
# def analysis_page():
#     return render_template("analysis.html",words = words,weights = weights)


# # 搜索界面
# @app.route('/search')
# def search_page():
#     form = SearchForm()
#     return render_template('search.html', form=form)


# # 搜索结果返回界面，返回时展示数据库中所有内容，包括正文文本
# @app.route('/news_result',methods=['POST','GET'])
# def newsResult_page():
#     form = SearchForm()
#     search = request.args.get("query")
#     search_list = []
#     cnn_search = pymysql.connect(host='127.0.0.1', user='root', password='1234', port=10306, database='gcz',
#                                  charset='utf8')
#     cursor_search = cnn_search.cursor()
#     sql_search = "select * from guanchazhe where content like '{}'".format('%'+search+'%')
#     print(sql_search)
#     cursor_search.execute(sql_search)
#     for item_search in cursor_search.fetchall():
#         search_list.append(item_search)
#     cursor_search.close()
#     cnn_search.close()
#     print(search_list)
#     return render_template("news_result.html", form=form, news=search_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5005,debug=True)
