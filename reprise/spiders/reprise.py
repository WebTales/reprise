import scrapy
import rubedo
import csv
import re
import params
from scrapy.http import Request

class RepriseSpider(scrapy.Spider):

    name = "reprise"
    start_urls = []
    type = []
    taxo = []
    workspaces = []
    with open(params.file, 'r') as f:
        for row in csv.reader(f.read().splitlines(),delimiter=';'):
            start_urls.append('http://'+row[0])
            type.append(row[1])
            taxo.append(row[2])
            workspaces.append(row[3])

    def start_requests(self):
        for indx, url in enumerate(self.start_urls):
            yield self.make_requests_from_url(url, {'index': indx})
    
    def make_requests_from_url(self, url, meta):
       return Request(url, callback=self.parse, dont_filter=True, meta=meta)
                   
    def parse(self, response):
    
        item_index = response.meta['index']
        originalUrl = response.request.meta['redirect_urls'][0]
        m = re.search(r'\d+',originalUrl)
        if m:
            contentId = m.group(0)
        else:
            contentId = None
        if contentId is not None:
            title = response.css('h1::text').extract_first()
            chapeau = title
            content = response.xpath('//*[@id="content"]')
            content = content.xpath('*[not(self::form or ancestor::form)]')
            content = content.xpath('*[not(@id="outils" or ancestor::div/@id="outils")]')
            texte = "".join(content.extract())
            visuel = response.xpath('//img[contains(@src, "arton")]/@src').extract_first()
            
            rubedo.insertContent(contentId, title, title, texte, visuel, self.type[item_index], self.taxo[item_index], self.workspaces[item_index])
        else:
            print(originalUrl)
            pass
