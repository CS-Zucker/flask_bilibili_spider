import jieba        #分词
from matplotlib import pyplot as plt    #绘图，数据可视化
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np                      #矩阵运算
import pymysql                          #数据库
import jieba.analyse

from spider.spider_data.database import Database



def draw_wordcloud(bv, text):
    
    img = Image.open(r'/home/featurize/work/git-flask/flask_bilibili_spider/demo_flask/App/static/assets/img/wordcloud-img/wordcloud-bg-3.jpg')   #打开遮罩图片
    img_array = np.array(img)   #将图片转换为数组
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path="git-flask/flask_bilibili_spider/demo_flask/App/static/spatial/assets/fonts/MSYH.TTC"
    )
    wc.generate_from_text(text)

    #绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')     #是否显示坐标轴

    plt.show()    #显示生成的词云图片

    #输出词云图片到文件
    plt.savefig('git-flask/flask_bilibili_spider/demo_flask/App/static/assets/img/wordcloud-img/{}.jpg'.format(bv),dpi=500)


if __name__ == "__main__":
    draw_wordcloud("BV1T94y1e74E", 'aaaa bbb b b b b cccc d d d dskdh s kjdhkahdjs ')















