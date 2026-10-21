import scrapy


class JumiaSpider(scrapy.Spider):
    name = "jumia"
    allowed_domains = ["jumia.co.ke"]
    start_urls = ["https://www.jumia.co.ke/laptops/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={"playwright":True},
                callback=self.parse
            )

    def parse(self, response):
        pass
