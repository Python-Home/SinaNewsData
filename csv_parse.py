import pandas
from datetime import datetime
from PIL import Image
from pyecharts import Bar, Line, Overlap, Map, Page, WordCloud
import re
from collections import Counter
from jieba import analyse, cut

df = pandas.read_csv(r'C:\Users\stefan\Desktop\results.csv', delimiter='#')

# 时间评论数量统计
d = df[:]['time'].apply(lambda x: x[5:13])
comment_df = pandas.DataFrame(d)
res = comment_df.groupby('time')['time'].count()
bar = Bar('天价账单', '新浪新闻', width='800')
bar.use_theme('macarons')
bar.add('每小时评论数', res.index, res)
bar.render('D://time.html')


# 评论地区统计
def area_select(area):
    china = ["北京", "天津", "上海", "重庆", "河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北",
             "湖南", "广东", "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾", "内蒙古", "广西", "西藏", "宁夏", "新疆", "香港", "澳门"]

    for item in china:
        if item in area:
            return item
    else:
        return '海外'


def em_select(content):
    pattern = re.compile(r"\[[a-zA-Z\u4e00-\u9fa5]+\]")
    result = re.findall(pattern, content)
    return result


def em_map(em):
    em = set(em)
    em = list(em)
    return em


# 条形图显示地区
d = df[:]['area'].apply(area_select)
area_df = pandas.DataFrame(d)
res = area_df.groupby('area')['area'].count().sort_values(ascending=False)
bar = Bar('地区消息统计', '新浪新闻', width="600")
bar.use_theme('macarons')
bar.add('地区分布', res.index, res.values, xaxis_interval=0)
bar.render(path='D://area.html')

# 中国地图显示
china_map = Map('省份分布情况', width=1000, height=600)
china_map.add("各省评论的人数", res.index, res.values, maptype='china', is_visualmap=True,
              visual_range=[0, 3000], is_map_symbol_show=False, visual_text_color='#000',
              is_label_show=True)
china_map.render(path='D://china_map.html')
page = Page()
page.add(bar)
page.add(china_map)
page.render('D://page.html')

# 评论表情分析
df['em_list'] = df['content'].apply(em_select)
em_list = list(df['em_list'])
em_list = list(filter(lambda x: True if x else False, em_list))
em_list = map(em_map, em_list)
temp = em_list
em_list = []
for item in temp:
    em_list.append(item[0])
counter = Counter(em_list)
results = counter.most_common()
y_emojis, x_counts = zip(*results)
bar = Bar('表情使用情况')
bar.add('emojis', y_emojis[:10], x_counts[:10],
        xaxis_interval=0).render('D://emoji.html')

# 词频分析基于 jieba 库。
content_list = df['content'].values.tolist()
content_str = " ".join(content_list)
keywords = analyse.extract_tags(
    content_str, withWeight=True, topK=100, allowPOS=('ns', 'n'))
segment, count = zip(*keywords)
ciyun = pandas.DataFrame()
ciyun['segment'] = segment
ciyun['count'] = count
wordcloud = WordCloud(width=800, height=520)
wordcloud.add('词云', ciyun['segment'], ciyun['count'], word_size_range=[20, 50])
wordcloud.render('D://wordcloud.html')

# 词频分析，基于内置模块
# def get_n(word):
#     res = re.findall('^[\u4E00-\u9FFF]+$', word)
#     if res:
#         return True
#     else:
#         return False
#
#
# content_item = cut(content_str, )
# content_item_list = []
# for item in content_item:
#     if len(item) > 1:
#         content_item_list.append(item)
#
# content_item_list = filter(get_n, content_item_list)
#
# couter = Counter(content_item_list)
# res = couter.most_common()
# print(res)
