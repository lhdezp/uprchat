import scrapy
import json
import os
import re



class UprSpiderSpider(scrapy.Spider):
    name = "upr_spider"
    start_urls = ["http://www.upr.edu.cu/",
                  "https://eventos.upr.edu.cu/"]
    visited = []

    def clean_title(self, title: str) -> str:
        cleaned_title =  re.sub(r'[<>:"/\\|?*]', '', title)
        cleaned_title =  re.sub(r'[\n\t\r]', '', cleaned_title)
        return cleaned_title

    def write_document(self, data: dict) -> None:
        directory = "contents"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{data["title"]}.json")

        try:
            with open(filename, "x") as f:
                json.dump(data, f, indent=4)
        except FileExistsError:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("Error: " + str(e))

    def is_download_link(self, url: str) -> bool:
        extensions = ["pdf", "zip", "exe", "rar"]
        return any(ext in url for ext in extensions)

    def validate_url(self, url: str) -> bool:
        return ((url.startswith("http") and "upr.edu.cu" in url) or url.startswith("/")) and url not in self.visited and not self.is_download_link(url) and "mailto" not in url

    def parse(self, response):
        title = response.xpath('//title/text()').get()
        paragraphs = response.xpath('//p/text()').getall()
        main_content = ' '.join(paragraphs).strip()

        cleaned_title = self.clean_title(title)

        data = {
            "title": cleaned_title,
            "main_content": main_content
        }

        self.write_document(data)

        links = response.xpath('//a[@href]')
        for link in links:
            url = link.xpath('@href').get()
            if self.validate_url(url):
                self.visited.append(url)
                self.write_document(
                    {"title": "visited", "main_content": self.visited})
                yield response.follow(url, callback=self.parse)
