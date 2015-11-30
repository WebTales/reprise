import scrapy
import rubedo

class RepriseSpider(scrapy.Spider):
    name = "reprise"
    allowed_domains = ["calais.fr"]
    start_urls = [
        "http://www.calais.fr/spip.php?article2680",
        "http://www.calais.fr/spip.php?article145"
    ]

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
        


            
