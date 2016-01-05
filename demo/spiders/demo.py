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
    
        title = response.css('title::text').extract_first().encode('utf-8')
        
        subtitle = response.xpath('//*[@class="detail-title_subtitle"]/text()').extract_first().encode('utf-8')
        
        price = response.xpath('//*[@id="price"]/text()').extract_first().encode('utf-8')
        
        description = response.xpath('//input[(@type="hidden") and (@name="description")]/@value').extract_first().encode('utf-8')
        
        photo = response.xpath('//input[(@type="hidden") and (@name="urlphoto")]/@value').extract_first()
        
        ville = response.xpath('//input[(@type="hidden") and (@name="ville")]/@value').extract_first().encode('utf-8')
        
        codepostal = response.xpath('//input[(@type="hidden") and (@name="codepostal")]/@value').extract_first().encode('utf-8')
        
        typebien = response.xpath('//input[(@type="hidden") and (@name="typebien")]/@value').extract_first().encode('utf-8')
        
        surface = response.xpath('//input[(@type="hidden") and (@name="surface")]/@value').extract_first().encode('utf-8')
        
        data-boudingbox-northeast-latitude = response.xpath('//*[@id="resume__map_new"]/@data-boudingbox-northeast-latitude').extract_first().encode('utf-8')
        data-boudingbox-northeast-longitude = response.xpath('//*[@id="resume__map_new"]/@data-boudingbox-northeast-longitude').extract_first().encode('utf-8')
        data-boudingbox-southwest-latitude = response.xpath('//*[@id="resume__map_new"]/@data-boudingbox-southwest-latitude').extract_first().encode('utf-8')
        data-boudingbox-southwest-longitude = response.xpath('//*[@id="resume__map_new"]/@data-boudingbox-southwest-longitude').extract_first().encode('utf-8')        
        
        lat = (data-boudingbox-northeast-latitude + data-boudingbox-southwest-latitude)/2
        lon = (data-boudingbox-northeast-longitude + data-boudingbox-southwest-longitude)/2
        print(lat)
        print(lon)
               
        rubedo.insertContent(title, subtitle, price,description, photo, ville, codepostal, typebien, surface)

