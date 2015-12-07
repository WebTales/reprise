import scrapy
import rubedo
import csv
import re

class RepriseSpider(scrapy.Spider):
    start_urls = []
    with open("calais.csv", 'r') as f:
        for row in csv.reader(f.read().splitlines(),delimiter=';'):
            start_urls.append('http://'+row[0])
            print(row[1])
    name = "reprise"
    exit()
    allowed_domains = ["calais.fr"]

    def parse(self, response):
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
            images = content.xpath('.//img[not (contains(@src, "arton") or contains(@src, "puce"))]/@src').extract()
            rubedo.insertContent(contentId, title, title, texte, visuel, images)
        else:
            print(originalUrl)
            pass
