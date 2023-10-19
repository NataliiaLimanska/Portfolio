import scrapy


class PricescraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    form = scrapy.Field()
    code = scrapy.Field()
    company = scrapy.Field()

