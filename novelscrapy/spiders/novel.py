
import sys
import scrapy
from scrapy.exceptions import CloseSpider
from ..items import NovelscrapyItem


sub_header = "https://www.cool18.com/bbs4/"


class NovelSpider(scrapy.Spider):
    name = "novel"
    allowed_domains = ["www.cool18.com"]
    start_urls = ["https://www.cool18.com/bbs4/index.php?action=search&bbsdr=life6&act=threadsearch&app=forum&keywords=%E8%B1%AA%E4%B9%B3%E8%80%81%E5%B8%88%E5%88%98%E8%89%B3&submit=%E6%9F%A5%E8%AF%A2"]

    def parse_context(self, response):
        item_ = response.meta['item']
        context = response.xpath("/html/body/table[1]/tr[2]/td/pre/text()")
        context_str = ""
        for p in context:
            context_str += p.get()
        item_['novel_context'] = context_str
        # print(item_, "!!!!!!!!!!!!!!!")
        yield item_

    def parse(self, response):
        novel_items = []

        novel_result = response.xpath("/html/body/table[3]/tr/td/div")
        novel_cnt = len(novel_result)
        # print(novel_result.get())
        print(type(novel_result), len(novel_result))
        if novel_cnt == 0:
            # when there is no novel close spider.
            raise CloseSpider('novel_cnt is 0, closing spider.')

        # collect novel information
        for r_ in novel_result:
            item_ = NovelscrapyItem()

            item_['upload_user'] = r_.xpath('./span[@class="t_author"]/text()').get()
            item_['upload_time'] = r_.xpath('./span[@class="t_dateline"]/i/text()').get()
            item_['novel_href'] = r_.xpath('./span[@class="t_subject"]/a/@href').get()
            novel_name_result = r_.xpath('./span[@class="t_subject"]/a')
            novel_name_str_list = novel_name_result.xpath(".//text()")
            novel_name = ""
            for s_ in novel_name_str_list:
                novel_name += s_.get()
            item_['novel_name'] = novel_name

            yield scrapy.Request(
                url=sub_header + item_['novel_href'],
                callback=self.parse_context,
                meta={'item': item_}
            )


        # get next page result
        page_bottons = response.xpath("/html/body/table[2]/tr[3]/td/a")
        for page_button in page_bottons:
            button_href = page_button.xpath("./@href").get()
            button_name = page_button.xpath("./text()").get()
            if button_name == '下一页':
                print(f"href = {button_href}, name = {button_name}")
                yield scrapy.Request(
                    url=sub_header + button_href,
                    callback=self.parse
                )
