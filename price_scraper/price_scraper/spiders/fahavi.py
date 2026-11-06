from urllib.error import HTTPError
from urllib.request import urlopen, Request
from decimal import Decimal
import json
import scrapy
from urllib.parse import quote, urlencode


class FahaviSpider(scrapy.Spider):
    name = "fahavi"
    start_urls = ["https://fahavicomputers.co.ke/product/hp-zbook-firefly-14-g10-price-in-kenya/"]
    products_api_url = "http://localhost:8000/api/v1/products/"
    retailer_api_url = f"http://localhost:8000/api/v1/retailers/"
    retailer_listing_api_url = "http://localhost:8000/api/v1/retailer_listings/"
    price_history_api_url = "http://localhost:8000/api/v1/price-history/"
    canonical_product_name = "HP ZBook Firefly 14 G10 | Core i7 13th Gen…"
    retailer_name = "Fahavi Computers"
    retailer_website = "https://fahavicomputers.co.ke/"

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright":True,
                    "playwright_include_page":True
                },
                callback=self.parse
            )

    async def parse(self, response):
        product_url=response.url
        current_price=response.css("div.fh-pp__price b.is-sale::text").get()
        if current_price:
            current_price=current_price.split(" ")[-1]
        current_price = Decimal(current_price.replace(",", "").strip())
        availability = response.css("p.fh-pp__stock::text").get()
        is_available=(availability.strip().lower() == "in stock"
                      if availability else False
                      )
        product_data = self.get_existing_record(self.products_api_url, self.canonical_product_name)
        if not product_data:
            self.logger.error("Existing product not found: %s", self.canonical_product_name)
            return None
        product_id=product_data["id"]
        self.logger.info("Product ID: %s", product_id)
        self.save_retailer(product_id, product_url, current_price, is_available)
        return None

    def get_existing_record(self, endpoint, name):
        url = f"{endpoint}by-name/{quote(name, safe="")}"
        try:
            with urlopen(url, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            self.logger.error("Failed to retrieve record: %s", exc)
            return None

    def save_retailer(self, product_id, product_url, current_price, is_available):
        retailer_payload={
            "name": self.retailer_name,
            "website_url":self.retailer_website
        }

        request = Request(
            self.retailer_api_url,
            data=json.dumps(retailer_payload).encode("utf-8"),
            headers={"Content-Type":"application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=15) as response:
                retailer_data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 409:
                retailer_data=self.get_existing_record(self.retailer_api_url, self.retailer_name)
                if not retailer_data:
                    return None
            else:
                self.logger.error(
                    "Retailer API error %s: %s",
                    exc.code,
                    exc.read().decode("utf-8", errors="replace")
                )
        except Exception as exc:
            self.logger.error("Failed to save retailer: %s", exc)
        retailer_id=retailer_data["id"]
        return self.save_retailer_listing(product_id,
                                          retailer_id,
                                          product_url,
                                          current_price,
                                          is_available
                                          )

    def save_retailer_listing(self, product_id, retailer_id, product_url, current_price, is_available):
        listing_id = None

        listing_payload = {
            "retailer_id": retailer_id,
            "product_id": product_id,
            "product_url": product_url,
            "current_price": str(current_price),
            "currency": "KES",
            "is_available": is_available
        }

        request = Request(
            self.retailer_listing_api_url,
            data=json.dumps(listing_payload).encode("utf-8"),
            headers={"Content-Type":"application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=15) as response:
                listing_data = json.loads(response.read().decode("utf-8"))
                listing_id = listing_data["id"]
        except HTTPError as exc:
            if exc.code == 409:
                params = urlencode({"product_url":product_url})
                lookup_url=f"{self.retailer_listing_api_url}by-url?{params}"

                try:
                    with urlopen(lookup_url, timeout=15) as response:
                        listing_data=json.loads(response.read().decode("utf-8"))
                        listing_id=listing_data["id"]
                except Exception as lookup_error:
                    self.logger.error("Failed to retrieve existing listing: %s", lookup_error)
                    return None
        except Exception as exc:
            self.logger.error("Failed to save retailer listing: %s", exc)
        if listing_id is not None:
            self.save_price_history(listing_id, current_price)
        return listing_id


    def save_price_history(self, listing_id, current_price):
        price_payload = {
            "listing_id": listing_id,
            "price": str(current_price),
            "currency": "KES"
        }

        request = Request(
            self.price_history_api_url,
            data=json.dumps(price_payload).encode("utf-8"),
            headers={"Content-Type":"application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=15) as response:
                price_data = json.loads(response.read().decode("utf-8"))
            return price_data
        except HTTPError as exc:
            self.logger.error(
                "Price History API error: %s",
                exc.code,
                exc.read().decode("utf-8", errors="replace")
            )
            return  None
        except Exception as exc:
            self.logger.error(
                "Failed to save price: %s",
                exc
            )
            return None


