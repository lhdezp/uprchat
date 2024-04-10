"""
    Modulo central del crawler de los sitios de uprChat
"""
from re import sub
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from parses import parse_docs


class UprSpider(Spider):
    """
        Spider principal para el crawler de uprChat
    """
    name = 'upr_spider'
    allowed_domains = [
        'upr.edu.cu'
    ]
    feed_uri = 'Contents.json'
    start_urls = ["http://www.upr.edu.cu/"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': feed_uri,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_OVERWRITE': True
    }
    link_extractor = LinkExtractor(allow_domains=['upr.edu.cu'])

    contents_types = {
        "html":"text/html" ,
        "json":"application/json" ,
        "txt":"text/plain" ,
        "pdf":"application/pdf" ,
        "jpeg":"image/jpeg" ,
        "png":"image/png" ,
        "gif":"image/gif" ,
        "doc": 'application/msword',
        'docx': "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    def clean_title(self, title: str) -> str:
        """Clean the web site title from problematic characters

        Args:
            title (str): Title of the web site with problematic characters

        Returns:
            str: Title of the web site with problem characters removed
        """
        cleaned_title = sub(r'[<>:"/\\|?*]', '', title)
        cleaned_title = sub(r'[\n\t\r]', '', cleaned_title)
        return cleaned_title

    def validate_url(self, url: str) -> bool:
        """Validate the url to visit

        Args:
            url (str): url to validate

        Returns:
            bool: True if the url is valid and else False
        """
        return  "mailto" not in url

    def parse(self, response):
        data = ""
        try:
            content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
            print(content_type)
            if content_type == self.contents_types['html']:
                title = response.xpath('//title//text()').get()
                content = response.xpath('//body//text()').getall()
                if not title :
                    title = response.xpath('//h1//text()').get()
                data = {
                "title": title,
                "content": content
                }
            elif content_type == self.contents_types['json']:
                plain_text = response.text
                data = {
                    "title": f'url: {response.url}',
                    "content": f'JSON content: {plain_text}',
                    }
            elif self.contents_types['pdf'] == 'application/pdf':
                data = parse_docs(response)
            elif 'image' in content_type:
                print(f"url:{response.url} content is a image")
        except Exception as e:
            data = {
                "error":f'{str(e)}',
                "url": f'{response.url}',
                "content": f'{response.content}'
            }
        finally:
            yield data
        for link in self.link_extractor.extract_links(response):
            url = link.url
            if self.validate_url(url):
                yield response.follow(url, callback = self.parse)



if __name__ == '__main__':

    process = CrawlerProcess()
    process.crawl(UprSpider)
    process.start()
