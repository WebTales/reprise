import scrapy
import rubedo
import csv
import re
import params
from scrapy.http import Request

class DemoSpider(scrapy.Spider):

    name = "demo"
    start_urls = []
    with open(params.file, 'r') as f:
        for row in csv.reader(f.read().splitlines(),delimiter=';'):
            start_urls.append('http://'+row[0])

    def start_requests(self):
        for indx, url in enumerate(self.start_urls):
            yield self.make_requests_from_url(url, {'index': indx})
    
    def make_requests_from_url(self, url, meta):
       return Request(url, callback=self.parse, dont_filter=True, meta=meta)
                   
    def parse(self, response):
    
        title = response.css('h1::text').extract_first()
        subtitle = response.xpath('//*[@class="detail-title_subtitle"]/text()').extract_first()
        price = response.xpath('//*[@id="price"]/text()').extract_first()
        description = response.xpath('//*[@class="description"]/text()').extract_first()
        photo = response.xpath('//input[(@type="hidden") and (@name="urlphoto")]/@value')
        print(title.encode('utf-8'))
        print(subtitle.encode('utf-8'))
        print(price.encode('utf-8'))
        print(description.encode('utf-8'))
        print(photo)
        #chapeau = title
        #content = response.xpath('//*[@id="content"]')
        #content = content.xpath('*[not(self::form or ancestor::form)]')
        #content = content.xpath('*[not(@id="outils" or ancestor::div/@id="outils")]')
        #texte = "".join(content.extract())
        #visuel = response.xpath('//img[contains(@src, "arton")]/@src').extract_first()
        
        #rubedo.insertContent(contentId, title, title, texte, visuel, params.type, "", "")

