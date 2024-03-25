import scrapy
import os

class UPRSpider(scrapy.Spider):
    name = 'upr_spider' #Nombre del spider
    start_urls = ['http://www.upr.edu.cu/'] #url de inicio
    allowed_domains=['upr.edu.cu'] #dominios de busqueda
    output_directory = 'scraped_data'  # Directorio para guardar los archivos .txt

    def parse(self, response):
        # Extraer el texto de la página actual
        page_text = response.xpath('//body//text()').getall()

        # Crear un nombre de archivo único para cada página
        filename = f'{self.output_directory}/{response.url.split("/")[-2]}.txt'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Guardar el texto en un archivo .txt correspondiente a la página
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('\n'.join(page_text).strip())

        # Seguir los enlaces en la página actual
        for next_page in response.css('a::attr(href)').getall():
            yield response.follow(next_page, callback=self.parse)
    