from gc import callbacks
import scrapy

from pricescraper.items import ProductItem

class PricesSpider(scrapy.Spider):
    name = 'pricespider'
    allowed_domains = ['mycare.de']
    start_urls = [
        'https://www.mycare.de/online-shop/rezeptpflichtige-medikamente/seite/1']

    def parse(self, response):
        # Extract all product URLs on the page
        product_urls = response.css('a[data-id="data-link-details"]::attr(href)').getall()
        unique_product_urls = list(set(product_urls))

        # Iterate through the prices and product URLs together
        for product_url in unique_product_urls:
            full_product_url = 'https://www.mycare.de' + product_url
            yield response.follow(full_product_url,
                                  callback=self.parse_product_page)

        for page_num in range(1, 19):
            next_page_url = f'https://www.mycare.de/online-shop/rezeptpflichtige-medikamente/seite/{page_num}'
            yield response.follow(next_page_url, callback=self.parse)

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG'
    }

    def parse_product_page(self, response):
        product_item = ProductItem()
        product_item['title'] = response.css('h1.element-name::text').get()
        product_item['url'] = response.url
        product_item['price'] = response.css('span.price::text').get()
        product_item['form'] = response.css('dl.row.mb-4.mb-sm-0 dt:contains("Inhalt:") + dd::text').get()
        product_item['code'] = response.css('dl.row.mb-4.mb-sm-0 dt:contains("PZN:") + dd::text').get()
        product_item['company'] = response.css('dl.row.mb-4.mb-sm-0 dt:contains("Hersteller:") + dd::text').get()

        yield product_item

