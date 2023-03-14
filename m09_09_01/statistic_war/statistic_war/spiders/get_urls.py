import re

import scrapy


class GetUrlsSpider(scrapy.Spider):
    name = "get_urls"
    allowed_domains = ["index.minfin.com.ua"]
    start_urls = ["https://index.minfin.com.ua/ua/russian-invading/casualties"]

    def parse(self, response, *args):
        prefix = "/month.php?month="
        links = response.xpath("//div[@class='ajaxmonth']/h4/a")
        for link in response.xpath("//div[@class='ajaxmonth']/h4/a"):
            yield {
                "link": prefix + re.search(r"\d{4}-\d{2}", link.xpath("@href").get()).group()
            }