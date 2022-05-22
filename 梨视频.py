import requests
import os
from lxml import etree
import random
import time
import re


class PearVideo():  # 定义梨视频类
    def __init__(self):
        self.start_url = 'https://www.pearvideo.com/author_11852721'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

    def get_video_url(self):  # 获取单个视频的地址和countId
        resp = requests.get(self.start_url, headers=self.headers).text
        tree = etree.HTML(resp)
        li_list = tree.xpath('.//ul[@class="category-list clearfix"]/li')
        video_urls = []
        countId_list = []
        video_names = []
        for li in li_list:
            video_url = li.xpath('./div[1]/a/@href')[0]
            countId = video_url.split('_')[-1]
            countId_list.append(countId)
            video_name = li.xpath('.//div[@class="vervideo-title"]/text()')[0]
            mrd = random.random()
            video_url = 'https://www.pearvideo.com/videoStatus.jsp?contId={}&mrd={}'.format(countId, mrd)
            video_urls.append(video_url)
            video_names.append(video_name)
        #print(video_urls)
        return video_urls, countId_list, video_names

    def get_download_url(self):  # 获取视频的真实下载地址，请求头中要携带refer参数，不然得不到想要的json数据
        video_urls, countId_list, video_names = self.get_video_url()
        download_urls = []
        for url, countId in zip(video_urls, countId_list):
            resp = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Referer': 'https: // www.pearvideo.com / video_{}'.format(countId)
            }).json()
            time.sleep(1)
            # print(resp)
            download_url = resp['videoInfo']['videos']['srcUrl']
            download_url = re.sub('/[0-9]+-', '/cont-{}-'.format(countId), download_url)
            # print(download_url)
            # time.sleep(1)
            download_urls.append(download_url)
        # print(download_urls)
        return download_urls, video_names

    # def download_video(self):  # 视频的保存
    #
    #     download_urls, video_names = self.get_download_url()
    #     # print(download_urls)
    #     filename = 'D://pearvideo'  #视频保存在d盘的pearvideo文件夹下
    #     if not os.path.exists(filename):
    #         os.mkdir(filename)
    #     index = 0
    #     for url in download_urls:
    #         with open('{}/{}.mp4'.format(filename, video_names[index]), mode='wb') as f:
    #             resp = requests.get(url, headers=self.headers).content
    #             # print(resp)
    #             f.write(resp)
    #             time.sleep(1)
    #         index += 1


if __name__ == '__main__':
    pearvideo_spider = PearVideo()
    re = pearvideo_spider.get_download_url()
    print(re)