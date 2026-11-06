import scrapy

class DigitoniaSpider(scrapy.Spider):
    name="digitonia"
    start_urls = ["https://www.digitonia.co.ke/product/hp-zbook-firefly-14-g10-intel-core-i7-13th-gen-16gb-ram-512gb-ssd-14-0%E2%80%B3-display-laptop/"]


    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={
                    "playwright":True,
                    "playwright_include_page":True
                },
                callback=self.parse
            )
    async def parse(self, response):
        self.logger.info("Digitonia product loaded successfully!")