import scrapy
from ..items import AmazonproItem
import re
# import pymysql


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = []
    url = []
    page_num = 1

    def __init__(self, kw=None, *args, **kwargs):
        # self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='...', db='Amazon',
        #                             charset='utf8')
        # self.cursor = self.conn.cursor()
        # kw = self.cursor.execute("SELECT keyword FROM keyword WHERE status = 1").fetch()
        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)
        k = kw.replace(' ', '+')
        print('keyword: ' + kw)
        self.name = kw
        self.start_urls = ['https://www.amazon.com/s?k=%s' % k]
        self.url = self.start_urls[0] + "&page=%d"

    def parse_detail(self, response):
        item = response.meta['item']
        rank = response.xpath('//div[@class="a-section table-padding"]//tr[last()-1]//span/span//text()').extract()
        if not rank:
            rank = "暂无排名"
        else:
            rank = ''.join(rank)
            try:
                rank = re.sub('\\(.*?\\)', '', rank)  # 去除括号内的文字
            except Exception as e:
                print(e)
                rank = rank
        item['rank'] = rank
        yield item

    def parse(self, response):

        title = response.xpath('//div[@id="search"]/div[1]/div[1]/div/span[3]/div['
                               '2]/div/div/div/div/div/div/div/h2/a/span/text() | //div['
                               '@id="search"]/div/div/div/span/div/div/div/div/div/div/div/div/div/div/div/h2/a/span'
                               '/text() | //div[@id="search"]/div[1]/div[1]/div/span[3]/div['
                               '2]/div/div/span/div/div/div/div/h2/a/span/text()').extract()
        detail_url = response.xpath('//div[@id="search"]/div[1]/div[1]/div/span[3]/div['
                                    '2]/div/div/div/div/div/div/div/h2/a/@href | //div['
                                    '@id="search"]/div/div/div/span/div/div/div/div/div/div/div/div/div/div/div/h2/a'
                                    '/@href | //div[@id="search"]/div[1]/div[1]/div/span[3]/div['
                                    '2]/div/div/span/div/div/div/div/h2/a/@href').extract()
        for i in range(len(detail_url)):
            basic_url = "https://www.amazon.com"
            item = AmazonproItem()
            item['title'] = title[i]
            item['keyword_rank'] = (i + 1) * self.page_num
            item['asin'] = detail_url[i].split('/')[-2]
            yield scrapy.Request(url=basic_url + detail_url[i], callback=self.parse_detail, meta={'item': item})
        # 实现全站数据爬取
        self.page_num += 1
        if self.page_num <= 3:
            new_url = self.url % self.page_num
            self.page_num += 1
            yield scrapy.Request(url=new_url, callback=self.parse)

    # def close(self, spider):
    #     self.cursor.close()
    #     self.conn.close()
