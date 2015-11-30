import scrapy
import rubedo
import csv

class RepriseSpider(scrapy.Spider):
    l = []
    with open("calais.csv", 'r') as f:
        for row in csv.reader(f.read().splitlines()):
        l.append(row)
    print l[0]
    start_urls = l[0]
    name = "reprise"
    allowed_domains = ["calais.fr"]

    def parse(self, response):
        title = response.css('h1::text').extract_first()
        chapeau = title
        content = response.xpath('//*[@id="content"]')
        content = content.xpath('*[not(self::form or ancestor::form)]')
        content = content.xpath('*[not(@id="outils" or ancestor::div/@id="outils")]')
        texte = "".join(content.extract())
        visuel = response.xpath('//img[contains(@src, "arton")]/@src').extract_first()
        images = content.xpath('.//img[not (contains(@src, "arton") or contains(@src, "puce"))]/@src').extract()

        rubedo.insertContent(title, title, texte, visuel, images)
        


            
