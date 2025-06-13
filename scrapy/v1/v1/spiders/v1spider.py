from pathlib import Path   
import scrapy
from v1.items import V1Item
from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider) :
    name = "v1"
   
    start_urls = ["https://www.car-encheres.fr/categorie-produit/nice/le-14-juin-2025/"]

    def parse(self,response):
        # quote=response.css('li.product')
        test = response.xpath("//title")
        for quote in response.css('ul.products li.product'):
                        yield {"car" : quote.css('div.container-product-list-info > h2.woocommerce-loop-product__title::text').get(),
                                "price": quote.css('span.woocommerce-Price-amount > bdi::text').get(),
                                "energy" : quote.XPATH('.//li[contains(., Carburant)]::text').get(),
                                "km": quote.XPATH('.//li[contains(., Kilométrage)]::text').get(),
                                }
            
            # loader = ItemLoader(item=V1Item(), selector=quote)
            # loader.add_css('car','div.container-product-list-info > h2 > span.text-uppercase')
            # loader.add_css('price','span.woocommerce-Price-amount > bdi::text')
            # # loader.add_css('vendor','div.tags a.tag::text')          
            # yield loader.load_item


            # yield {"text" : quote.css('span.text::text').get(),
            #        "author": quote.css('small.author::text').get(),
            #        'tags': quote.css('a.tag::text').getall()
            #        }
            # yield from response.follow_all(css='li.next a',callback = self.parse)
            

        # for href in response.css('li.next a::attr(href)'):
        #         yield response.follow(href,callback=self.parse)
            
        # next_page = response.css('li.next a::attr(href)').get()

        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.request(next_page, callback=self.parse)
