import os
import re
import threading
import time
from multiprocessing.dummy import Pool
from time import sleep

import requests
from lxml import etree
#需求：爬取梨视频的视频数据
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
}

urls = []  # 用于保存视频下载的所有链接
def init():

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    #原则：线程池处理的是阻塞且较为耗时的操作

    url='https://www.pearvideo.com/category_5'
    page_text=requests.get(url=url,headers=headers).text

    tree=etree.HTML(page_text)

    li_list=tree.xpath('//ul[@id="listvideoListUl"]/li')

    #获取响应体中的链接
    ex='video_([0-9]+)' #用于获取视频id的模式
    #需要被替换的模式
    ex1='[third,adshort]/.*?/(.*?)-.*?'


    for li in li_list:
        detail_url='https://www.pearvideo.com/'+li.xpath('./div/a/@href')[0]
        name=li.xpath('./div/a/div[2]/text()')[0]+'.mp4'
        con_id=re.findall(ex,li.xpath('./div/a/@href')[0])[0]

        #对详细页的url发起请求
        headers = {
            'Referer':detail_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        }
        session = requests.Session()
        #从详细页中解析处视频的地址(url)

        json_url='https://www.pearvideo.com/videoStatus.jsp?contId='+con_id
        response=session.get(url=json_url,headers=headers)
        dic_obj=response.json()
        #被伪装的下载地址

        down_url=dic_obj['videoInfo']['videos']['srcUrl']
        print('视频下载链接为：' + down_url)

        #将响应体中的链接转化为真实链接
        need_replace=re.findall(ex1,down_url)[0]
        #print(need_replace)

        #替换的字符串
        replaced='cont-'+con_id
        #真实的下载地址
        down_url=down_url.replace(need_replace,replaced)

        dic={
            'name':name,
            'url':down_url
        }
        urls.append(dic)
#下载视频
def down(dic):
    url=dic['url']
    name=dic['name']
    print(name,'正在下载...')

    resPage=requests.get(url=url,headers=headers)
    #print(resPage.status_code)

    # 创建文件夹
    if not os.path.exists('../pearvideoLibs'):
        os.mkdir('../pearvideoLibs')
    video_path='../pearvideoLibs/'+name
    if resPage.status_code==200:
        with open(video_path,'wb') as fp:
            fp.write(resPage.content)
        print(name,'下载完成')

if __name__=="__main__":


    '''
    time_start = time.time()
    init()

    for dic in urls:
        down(dic)
    time_end = time.time()
    print("%d second" % (time_end - time_start))
    '''


    time_start = time.time()
    init()
    mypool = Pool(4)
    mypool.map(down, urls)
    time_end = time.time()

    mypool.close()
    mypool.join()
    print("%d second" % (time_end - time_start))