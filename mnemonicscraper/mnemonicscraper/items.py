# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

class MnemonicscraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    ingress = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    content = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join())
    url = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    subcategory = scrapy.Field(output_processor=TakeFirst())

    pass
