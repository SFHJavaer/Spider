import csv
import codecs
import requests  # 导入requests包
from bs4 import BeautifulSoup  # 导入bs4包
from datetime import datetime


class Produce:
    price_data = []  # 农产品的价格数据列表
    item_name = ""  # 农产品的类别名

    def __init__(self, category):
        self.item_name = category
        self.price_data = []

    # 读取某一页的数据，默认是第一页
    def get_price_page_data(self, page_index=1):
        url = 'http://www.wbncp.com/PriceQuery.aspx?PageNo=' + str(
            page_index) + '&ItemName=' + self.item_name + '&DateStart=2017/10/1&DateEnd=2020/3/31 '
        strhtml = requests.get(url)  # GET方式，获取网页数据
        # print(strhtml.text)
        soup = BeautifulSoup(strhtml.text, 'html.parser')  # 解析网页文档
        # print(soup)

        table_node = soup.find_all('table')
        # number = 0
        # for table in table_node:
        #     number += 1
        #     print(number, table)
        all_price_table = table_node[21]  # 获取含有农产品价钱的table的数据
        # print(all_price_table)
        for tr in all_price_table.find_all('tr'):
            number = 0
            price_line = []
            for td in tr.find_all('td'):
                number += 1
                # print(number, td)
                if number == 1:
                    price_line.append(td.get_text().split())  # 获取品名
                elif number == 2:
                    price_line.append(td.get_text().split())  # 获取产地
                elif number == 3:
                    price_line.append(td.get_text().split())  # 获取规格
                elif number == 4:
                    price_line.append(td.get_text().split())  # 获取单位
                elif number == 5:
                    price_line.append(td.get_text().split())  # 获取最高价
                elif number == 6:
                    price_line.append(td.get_text().split())  # 获取最低价
                elif number == 7:
                    price_line.append(td.get_text().split())  # 获取均价
                elif number == 8:
                    price_line.append(datetime.strptime(td.get_text().replace('/', '-'), '%Y-%m-%d'))  # 获取日期
            self.price_data.append(price_line)
        return

    # 获取全部页面的数据
    def get_price_data(self):
        for i in range(33):
            self.get_price_page_data(str(i))
        return

    # 讲爬虫的数据写入到CSV文件，路径为：D:\Data_pytorch\名字.csv
    def data_write_csv(self):  # file_address为写入CSV文件的路径，self.price_data为要写入数据列表
        self.get_price_data()
        file_address = "D:\Data_pytorch\\" + self.item_name.__str__() + ".csv"
        file_csv = codecs.open(file_address, 'w+', 'utf-8')  # 追加
        writer = csv.writer(file_csv, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for temp_data in self.price_data:
            writer.writerow(temp_data)
        print(self.item_name + "爬虫数据保存到文件成功！")

    # 以字典类型读取csv文件,读取路径为：D:\Data_pytorch\名字.csv
    def data_reader_csv(self):
        file_address = "D:\Data_pytorch\\" + self.item_name.__str__() + ".csv"
        with open(file_address, 'r', encoding='utf8')as fp:
            # 使用列表推导式，将读取到的数据装进列表
            data_list = [i for i in csv.DictReader(fp, fieldnames=None)]  # csv.DictReader 读取到的数据是list类型
        print(self.item_name + "数据如下：")
        print(data_list)
        return data_list


list = ["茭白", "西红柿","佛手瓜"]
for temp_name in list:
    produce = Produce(temp_name)
    produce.data_write_csv()
    data = produce.data_reader_csv()
