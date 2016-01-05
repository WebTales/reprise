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
            start_urls.append(row[0])

    def start_requests(self):
        for indx, url in enumerate(self.start_urls):
            yield self.make_requests_from_url(url, {'index': indx})
    
    def make_requests_from_url(self, url, meta):
       return Request(url, callback=self.parse, dont_filter=True, meta=meta)
                   
    def parse(self, response):
    
        title = response.css('title::text').extract_first().encode('utf-8')
        
        try:
            subtitle = response.xpath('//*[@class="detail-title_subtitle"]/text()').extract_first().encode('utf-8')
        except:
            subtitle = ""
        
        try:
            price = response.xpath('//*[@id="price"]/text()').extract_first().encode('utf-8')
        except:
            price = ""
        
        try:            
            description = response.xpath('//input[(@type="hidden") and (@name="description")]/@value').extract_first().encode('utf-8')
        except:
            description = ""
            
        photo = response.xpath('//input[(@type="hidden") and (@name="urlphoto")]/@value').extract_first()

        try:          
            ville = response.xpath('//input[(@type="hidden") and (@name="ville")]/@value').extract_first().encode('utf-8')
        except:
            ville = ""
        
        try:          
            codepostal = response.xpath('//input[(@type="hidden") and (@name="codepostal")]/@value').extract_first().encode('utf-8')
        except:
            codepostal = ""
        
        try:
            typebien = response.xpath('//input[(@type="hidden") and (@name="typebien")]/@value').extract_first().encode('utf-8')
        except:    
            typebien = ""
                
        try:
            surface = response.xpath('//input[(@type="hidden") and (@name="surface")]/@value').extract_first().encode('utf-8')
         except:
            surface = ""
                
        try:
            northeastLatitude = response.xpath('//div[@id="resume__map_new"]/@data-boudingbox-northeast-latitude').extract_first().encode('utf-8')
            northeastLongitude = response.xpath('//div[@id="resume__map_new"]/@data-boudingbox-northeast-longitude').extract_first().encode('utf-8')
            southwestLatitude = response.xpath('//div[@id="resume__map_new"]/@data-boudingbox-southwest-latitude').extract_first().encode('utf-8')
            southwestLongitude = response.xpath('//div[@id="resume__map_new"]/@data-boudingbox-southwest-longitude').extract_first().encode('utf-8')        
            
            lat = (float(northeastLatitude) + float(southwestLatitude))/2
            lon = (float(northeastLongitude) + float(southwestLongitude))/2
        except:
            lat=0
            lon=0
            
        rubedo.insertContent(title, subtitle, price,description, photo, ville, codepostal, typebien, surface, lat, lon)

