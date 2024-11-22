# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
import json
# from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv
import os

class MongoDBNhanamscrapePipeline:
    def __init__(self):
        # Connection String
        econnect = str(os.environ['Mongo_HOST']) #thiết lập biến môi trường cho triển khai Docker phần 3.
        # self.client = pymongo.MongoClient('mongodb://localhost:27017') #Cho phần đưa dữ liệu lên MongoDB ở phần 2.
        self.client = pymongo.MongoClient('mongodb://'+econnect+':27017')
        self.db = self.client['dbnhanamcrawler'] #Create Database      
        pass
    
    def process_item(self, item, spider):
        collection =self.db['tblnhanam'] #Table
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")       
        pass
class JsonDBNhanamscrapePipeline:
    def process_item(self, item, spider):
        with open('jsondatanhanamscrape.json', 'a', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(line)
        return item
    
class CSVDBNhanamscrapePipeline:
    '''
    mỗi thông tin cách nhau với dấu $
    Ví dụ: coursename$lecturer$intro$describe$courseUrl
    Sau đó, cài đặt cấu hình để ưu tiên Pipline này đầu tiên
    '''
    def process_item(self, item, spider):
        with open('csvdatanhanamscrape.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='$')
            writer.writerow([
                item['name'],
                item['price'],
                item['category'],
                item['subcategory'],
                item['size'],
                item['pages'],
                item['publishing_affiliate'],
                item['barcode'],
                item['seller'],
                item['in_stock'],
                item['description']
            ])
        return item
    pass