import json
import scrapy
from urllib.request import Request, urlopen


class LappyWorldSpider(scrapy.Spider):
    name = "lappyworld"
    start_urls = ["https://laptopsworld.co.ke/"]
    target_product_id="5812"
    target_product_name="HP EliteBook x360 1030 G3"
    api_url="http://localhost:8000/api/v1/products/"

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
        card = response.css(f"div.wd-product[data-id='{self.target_product_id}']")
        if not card:
            self.logger.warning("Product ID not found", self.target_product_id)
            return
        name = card.css(
            "h3.wd-entities-title a::text"
        ).get()
        if not name or name.strip() != self.target_product_name:
            self.logger.warning("Product name did not match")
            return
        category=card.css(
            ".wd-product-cats a::text"
        ).get()

        payload= {
            "name":name.strip(),
            "brand":"HP",
            "model_number":"x360 1030 G3",
            "category":category.strip() if category else None
        }

        request = Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type":"application/json"},
            method="POST"
        )
        try:
            with urlopen(request, timeout=15) as api_response:
                self.logger.info(
                    "Product saved: %s | API status %s",
                    name.strip(),
                    api_response.status
                )
        except Exception as exc:
            self.logger.error(
                "Failed to send product to API %s", exc
            )



