from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from queue import Queue
from jsonpath import jsonpath
import csv
import re
import time

url_queue = Queue()
result = set()


def init_url():
    for item in range(200):
        url = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=kj&newsid=comos-hkhfqnt3236918&group=0&compress=0&ie=gbk&oe=gbk&page={}&page_size=20&jsvar=loader_{}_25322325".format(
            item, int(time.time() * 1000))
        url2 = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-hkhfqnt7246449&group=0&compress=0&ie=gbk&oe=gbk&page={}&page_size=20&jsvar=loader_{}_25322325".format(
            item, int(time.time() * 1000))
        url3 = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=sh&newsid=comos-hkhfqns9406485&group=0&compress=0&ie=gbk&oe=gbk&page={}&page_size=200&jsvar=loader_aaaaaa_90151836".format(
            item)
        url_queue.put(url3)


def fetch():
    while not url_queue.empty():
        url = url_queue.get()
        current_url = url.replace('aaaaaa', str(int(time.time() * 1000)))
        response = requests.get(current_url)
        parse(response.json())
        print(current_url)


def parse(json_data):
    comment_list = jsonpath(json_data, '$.result..content')
    nick_list = jsonpath(json_data, '$.result..nick')
    area_list = jsonpath(json_data, '$.result..area')
    time_list = jsonpath(json_data, '$.result..time')
    ip_list = jsonpath(json_data, '$.result..ip')
    try:
        for nick, comment, time, area, ip in zip(nick_list, comment_list, time_list, area_list, ip_list):
            result.add((nick, comment, time, area, ip))
    except TypeError as e:
        print(e)


def save():
    with open(r'C:\Users\stefan\Desktop\results.csv', 'w', encoding='utf8', newline='') as file:
        for item in result:
            csvobject = csv.writer(file, delimiter="#")
            csvobject.writerow(item)


if __name__ == "__main__":
    init_url()
    exector = ThreadPoolExecutor(max_workers=50)
    tasks = []
    for item in range(20):
        tasks.append(exector.submit(fetch))
    results = as_completed(tasks)
    for item in results:
        pass
    save()
