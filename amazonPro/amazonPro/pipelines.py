# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AmazonproPipeline:
    def process_item(self, item, spider):
        spider.cursor.execute('INSERT INTO good_info (ASIN, title) VALUES (item["asin"], item["title"])')
        spider.cursor.execute('INSERT INTO keyword_order (keyword_order, category_order) VALUES (item["keyword_rank"], item["rank"])')
        spider.conn.commit()
        return item
