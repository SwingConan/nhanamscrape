# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class NhanamscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
   name = scrapy.Field()
   price = scrapy.Field()
   category = scrapy.Field()
   subcategory = scrapy.Field()
   size = scrapy.Field()
   pages = scrapy.Field()
   publishing_affiliate = scrapy.Field()
   barcode = scrapy.Field()
   seller = scrapy.Field()
   in_stock = scrapy.Field()
   description = scrapy.Field()
    
