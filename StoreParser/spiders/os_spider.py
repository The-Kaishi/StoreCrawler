import scrapy
from config import header


class OsSpider(scrapy.Spider):
    name = 'os'
    # allowed_domains = ['ozon.ru']
    start_urls = ['https://www.ozon.ru/category/smartfony-15502/?sorting=rating&tf_state=boOm8HfvRqBSfUvSaip-2Q6QaKqz5-E0KcFgKmVFArSOKV_TE4t-1kSI7g%3D%3D']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for link in response.css('div.k6s a::attr(href)'):
            yield response.follow(link, callback=self.parse_page)

        for _ in range(1, 2):
            next_page = f'https://www.ozon.ru/category/smartfony-15502/?page={_}&sorting=rating&tf_state=dVqWbmABozDoYi6BW1H4-EgHmBMvgdO99Wwu-avG1QBq8uen'
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        android_str = 'Android'
        ios_str = 'iOS'
        # if ios_str in response.css('dd.ly9 a::text').get().strip():
        #     yield {
        #         'version_os': response.css('dd.ly9 a::text').get().strip()
        #     }
        if android_str in response.css('dd.ly9::text').get().strip():
            yield{
                'version_os': response.css('dd.ly9::text').get().strip()
            }
