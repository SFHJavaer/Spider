import requests
import os
from lxml import etree
import time


def get_picture_url(page_url: str):
    # 确定目标网址
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    # 发送请求
    response = requests.get(url=page_url, headers=headers).text
    tree = etree.HTML(response)
    # 数据解析
    image_url = tree.xpath(
        '/html/body/div[1]/div/div[6]/div/div[2]/section/div[1]/section/section/section/section/article/section/span/picture/img/@data-src')
    # 1.xpath指定路径，上端路径可以截止到li层（或其他acticle等）标签，将li再进行一次xpath遍历
    # 2.或者直接指定其中一个爬取元素的完整路径，同时不对中间开始分层的列表标签进行索引指定，最后爬出来同样是不同分层目录下同样的标签或属性（所以如果是列表元素，不进行索引的唯一性指定，就会默认将列表全部爬取

    for image in image_url:
        video = 'https:' + image
        # print(video)
        url = image
        data_image = requests.get(url=video, headers=headers).content
        # print(data_image)
        # quit()
        ri = video.rindex('/')
        image_name = video[ri + 1:]
        with open(image_name, 'wb') as fp:
            fp.write(data_image)
            print('打印成功')
            print(image_name)
        time.sleep(0.5)


for i in range(1, 743):
    page_url_ = f"https://www.veer.com/search-image/lang/?sort=best&page={i}"
    get_picture_url(page_url_)
    print(i)
# 图片只要显示在网站上，那么在该网页就一定有相应的资源，不管是动态还是静态加载，加载完一定能获取到
# 对于进行双层访问才能获取到的资源，可以在子页面复制网址在父页面进行查找，即使查不到也可以找相似的字段，最后进行图片网址拼接来获取新资源
