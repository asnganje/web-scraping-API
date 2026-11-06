import json
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from decimal import Decimal
import scrapy
from urllib.request import Request, urlopen

class LappyWorldSpider(scrapy.Spider):
    name = "lappyworld"
    start_urls = ["https://laptopsworld.co.ke/"]
    target_product_id="30551"
    target_product_name="HP ZBook Firefly 14 G10 | Core i7 13th Gen…"
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
        product_url=card.css("h3.wd-entities-title a::attr(href)").get()
        if not product_url:
            self.logger.warning("Product URL not found")
            return
        current_price = card.css(
            ".price .woocommerce-Price-amount bdi::text"
        ).get()
        current_price = Decimal(
            current_price.replace("\xa0", "").replace(",", "").strip()
        )
        if not current_price:
            self.logger.warning("Price not found")
            return

        payload= {
            "name":name.strip(),
            "brand":"HP",
            "model_number":"ZBook Firefly 14 G10",
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
                product_data= json.loads(api_response.read().decode("utf-8"))
                product_id=product_data["id"]
                self.logger.info(
                    "Product created: %s",
                    product_id
                )
        except HTTPError as exc:
            if exc.code == 409:
                product_data=self.get_existing_record(self.api_url, name.strip())
                if not product_data:
                    return
                product_id = product_data["id"]
                self.logger.info("Existing product retrieved. ID: %s", product_id)
            else:
                self.logger.error("Product API error %s", exc)
                return

        self.save_retailer(product_id, product_url, current_price)
    def get_existing_record(self, endpoint, name):
        url=f"{endpoint}by-name/{quote(name, safe='')}"
        try:
            with urlopen(url, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            self.logger.error("Failed to retrieve existing record: %s", exc)
            return None


    def save_retailer(self, product_id, product_url, current_price):
        self.logger.info("Extracted price: %s", current_price)
        retailer_name="Laptops World"
        retailer_api_url="http://localhost:8000/api/v1/retailers/"
        payload={
            "name":retailer_name,
            "website_url":"https://laptopsworld.co.ke/"
        }

        request = Request(
            retailer_api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type":"application/json"},
            method="POST"
        )
        try:
            with urlopen(request, timeout=15) as response:
                retailer_data=json.loads(
                    response.read().decode("utf-8")
                )
                retailer_id=retailer_data["id"]
                self.logger.info(
                    "Retailer saved successfully. Status %s",
                    retailer_id
                )
        except HTTPError as exc:
            if exc.code == 409:
                self.logger.info("Retailer already exists")
                retailer_url = (
                    f"{retailer_api_url}by-name/"
                    f"{quote(retailer_name, safe='')}"
                )
                try:
                    with urlopen(retailer_url, timeout=15) as response:
                        retailer = json.loads(
                            response.read().decode("utf-8")
                        )
                        retailer_id=retailer["id"]
                except Exception as lookup_error:
                    self.logger.error(
                        "Failed to retrieve retailer info: %s",
                        lookup_error
                    )
                    return None

            else:
                self.logger.info("Retailer API error: %s", exc)
                return None
        except Exception as exc:
            self.logger.error("Failed to save retailer: %s", exc)
            return None
        self.save_retailer_listing(product_id, retailer_id, product_url, current_price)
        return None
    def save_retailer_listing(self, product_id, retailer_id, product_url, current_price):
        listing_api_url = "http://localhost:8000/api/v1/retailer_listings/"
        listing_id = None

        listing_payload={
            "retailer_id":retailer_id,
            "product_id":product_id,
            "product_url": product_url,
            "current_price": str(current_price),
            "currency": "KES",
            "is_available":True
        }
        request = Request(
            listing_api_url,
            data=json.dumps(listing_payload).encode("utf-8"),
            headers={"Content-Type":"application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=15) as response:
                listing_data = json.loads(response.read().decode("utf-8"))
                listing_id=listing_data["id"]
        except HTTPError as exc:
            if exc.code == 409:
                params=urlencode({"product_url":product_url})
                lookup_url=f"{listing_api_url}by-url?{params}"
                try:
                    with urlopen(lookup_url, timeout=15) as response:
                        listing_data = json.loads(response.read().decode("utf-8"))
                    listing_id = listing_data["id"]
                except Exception as lookup_error:
                    self.logger.error(lookup_error)
                    return None
            else:
                self.logger.error("Retailer listing API error %s: %s",
                                exc.code,
                                  exc.read().decode("utf-8", errors="replace")
                                  )
        except Exception as exc:
            self.logger.error("Failed to save retailer listing: %s", exc)
        if listing_id is not None:
           self.save_price_history(listing_id, current_price)
        return listing_id

    def save_price_history(self, listing_id, current_price):
        price_history_api_url="http://localhost:8000/api/v1/price-history/"

        price_payload={
            "listing_id":listing_id,
            "price":str(current_price),
            "currency":"KES"
        }

        request = Request(
            price_history_api_url,
            data=json.dumps(price_payload).encode("utf-8"),
            headers={"Content-Type":"application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=15) as response:
                price_data=json.loads(response.read().decode("utf-8"))
            return price_data
        except HTTPError as exc:
            self.logger.error(
                "Price History API error %s: %s",
                exc.code,
                exc.read().decode("utf-8", errors="replace")
            )
            return None
        except Exception as exc:
            self.logger.error(
                "Failed to save price: %s",
                exc
            )
            return None


