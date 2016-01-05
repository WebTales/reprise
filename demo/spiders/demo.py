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
        
        description = response.xpath('//input[(@type="hidden") and (@name="description")]/@value').extract_first()
        
        photo = response.xpath('//input[(@type="hidden") and (@name="urlphoto")]/@value').extract_first()
        
        ville = response.xpath('//input[(@type="hidden") and (@name="ville")]/@value').extract_first()
        
        codepostal = response.xpath('//input[(@type="hidden") and (@name="codepostal")]/@value').extract_first()
        
        typebien = response.xpath('//input[(@type="hidden") and (@name="typebien")]/@value').extract_first()
        
        surface = response.xpath('//input[(@type="hidden") and (@name="surface")]/@value').extract_first()
        
        caracteristiques = response.xpath('//ol[@class="description-liste"]/text()').extract_first()
        
        
        
        
        
        print(title.encode('utf-8'))
        print(subtitle.encode('utf-8'))
        print(price.encode('utf-8'))
        print(description.encode('utf-8'))
        print(photo)
        print(ville.encode('utf-8'))
        print(codepostal.encode('utf-8'))
        print(typebien.encode('utf-8'))
        print(surface.encode('utf-8'))
        print(caracteristiques.encode('utf-8'))
        #chapeau = title
        #content = response.xpath('//*[@id="content"]')
        #content = content.xpath('*[not(self::form or ancestor::form)]')
        #content = content.xpath('*[not(@id="outils" or ancestor::div/@id="outils")]')
        #texte = "".join(content.extract())
        #visuel = response.xpath('//img[contains(@src, "arton")]/@src').extract_first()
        
        #rubedo.insertContent(contentId, title, title, texte, visuel, params.type, "", "")

