import time
import requests
import os
from requests import RequestException
import json


def get_page(url):
    try:
        # 添加User-Agent，放在headers中，伪装成浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response
        return None
    except RequestException:
        return None


def parse_page(html, count, word):
    html = html.text
    if html:
        p = json.loads(html)['items']  # 转为json格式  提取items字段
        print(len(p))  # 图片数
        for i in p[:-1]:  # [0:5]前5张
            print(i['pic_url'])
            count = count + 1
            # 数据保存
            with open(word + '/' + word + '_url_搜狗.txt', 'a', encoding='utf-8') as f:
                f.write(i['pic_url'] + '\n')
            pic = get_page(i['pic_url'])
            if pic:
                with open(word + '/' + '搜狗_' + str(count) + '.jpg', 'wb') as f:
                    f.write(pic.content)
            time.sleep(1)

        return count


if __name__ == '__main__':
    word = '兔子'  # 关键词
    page = 50  # 爬取的页数
    count = 0  # 图片计数

    if not os.path.exists(word):
        os.makedirs(word)  # 建目录

    for i in range(page):
        url = 'https://pic.sogou.com/pics?query={}&mode=1&start={}&reqType=ajax&reqFrom=result&tn=0'.format(word,
                                                                                                            i * 48)
        # 发送请求、获取响应
        html = get_page(url)
        # 解析响应 数据存储
        count = parse_page(html, count, word)

        time.sleep(1)