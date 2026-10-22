from playwright.async_api import Page
import scrapy
from scrapy_playwright.page import PageMethod


class LappyWorldSpider(scrapy.Spider):
    name = "lappyworld"
    # allowed_domains = ["jumia.co.ke"]
    start_urls = ["https://laptopsworld.co.ke/"]
    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={"playwright":True,
                      "playwright_include_page": True,
                      "handle_httpstatus_list": [403]
                      },
                callback=self.parse
            )


    async def parse(self, response):
        page: Page = response.meta["playwright_page"]

        try:
            await page.wait_for_timeout(30_000)
        finally:
            await page.close()
            self.logger.info("Browser page closed.")

