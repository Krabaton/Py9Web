import json
import re
from datetime import datetime

import scrapy


def get_next_link():
    with open('links.json', 'r') as fd:
        r = json.load(fd)
    return [el.get('link') for el in r]


class GetLossesSpider(scrapy.Spider):
    name = "get_losses"
    allowed_domains = ["index.minfin.com.ua"]
    start_urls = ["https://index.minfin.com.ua/ua/russian-invading/casualties"]

    def parse(self, response, *_):
        result = {}
        for element in response.css('ul[class=see-also] li[class=gold]'):
            date = element.xpath('span/text()').get()
            try:
                date = datetime.strptime(date, "%d.%m.%Y").isoformat()
            except ValueError:
                print(f"error for {date}")
                continue

            result.update({"date": date})

            losses = element.xpath('div[@class="casualties"]/div/ul/li')
            for l in losses:
                # print(' '.join(l.css('*::text').extract()))
                title, quantity, *rest = ' '.join(l.css('*::text').extract()).split('—')
                title = title.strip()
                quantity = re.search(r"\d+", quantity).group()
                result.update({title: int(quantity)})
            yield result

        for next_link in get_next_link():
            yield scrapy.Request(self.start_urls[0] + next_link, method="GET")
