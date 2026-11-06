import scrapy
from decimal import Decimal

class DigitoniaSpider(scrapy.Spider):
    name="digitonia"
    start_urls = ["https://www.digitonia.co.ke/product/hp-zbook-firefly-14-g10-intel-core-i7-13th-gen-16gb-ram-512gb-ssd-14-0%E2%80%B3-display-laptop/"]
    api_url = "http://localhost:8000/api/v1/products/"
    retailer_name = "Digitonia Systems Ltd"
    retailer_website = "https://www.digitonia.co.ke/"

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

        name=response.css("h1::text").get()
        product_url =response.url
        current_price = response.css("p.price .woocommerce-Price-amount bdi::text").get()
        if current_price:
            current_price = Decimal(current_price.replace(",", "").strip())
        availability=response.css("span.availability-text::text").get()
        is_available=(availability.strip().lower()=="in stock"
                      if availability else False
                      )
        category="Laptops"
        brand="HP"
        model_number = "ZBook Firefly 14 G10"

