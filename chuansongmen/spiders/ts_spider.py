import scrapy
import time

class ts(scrapy.Spider):
    name = 'scrapy_spider'

    def start_requests(self):
        url = 'http://chuansong.me/account/tiny4voice'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
        post_list = response.css('div.feed_item')
        for post in post_list:
            yield {
                'title': post.css('a.question_link::text').extract_first().strip(),
                'url': 'http://chuansong.me' + post.css('a.question_link::attr(href)').extract_first().strip(),
                'published_at': post.css('span.timestamp::text').extract_first()
            }

        next_page = response.xpath('//a[contains(@href, "start") and @style="float: right"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            time.sleep(5)
            yield scrapy.Request(next_page, callback=self.parse)
