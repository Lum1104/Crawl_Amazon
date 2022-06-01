# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

class AmazonproPipeline:
    fp = None

    def open_spider(self, spider):
        # if not os.path.exists("./%s.txt" % spider["name"]):
        #     self.fp = open("./%s.txt" % spider["name"], 'w', encoding='utf-8')
        self.fp = open("./%s.txt" % spider.name, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        # spider.cursor.execute('INSERT INTO good_info (ASIN, title) VALUES (item["asin"], item["title"])')
        # spider.cursor.execute('INSERT INTO keyword_order (keyword_order, category_order) VALUES (item["keyword_rank"], item["rank"])')
        # spider.conn.commit()

        asin = item["asin"]
        keyword_rank = item["keyword_rank"]
        rank = item["rank"]
        title = item["title"]
        # print(spider.name)
        self.fp.write('title: ' + title + ', asin: ' + asin + ', keyword_rank: ' + str(keyword_rank) + ', rank: ' + rank + '\n')
        return item

    def close_spider(self, spider):
        self.fp.write("--------------------------------------------------------------\n")
        self.fp.write("--------------------------------------------------------------\n")
        self.fp.write("--------------------------------------------------------------\n")
        self.fp.close()
