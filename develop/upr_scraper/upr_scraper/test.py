import unittest
from unittest.mock import patch
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerProcess
from upr_spider import UprSpider

class TestUprSpider(unittest.TestCase):
    def setUp(self):
        self.spider = UprSpider()

    @patch('crawler_module.parse_docs')
    def test_parse(self, mock_parse_docs):
        # Mock response data
        title = 'Example Title'
        content = 'Example Content'
        url = 'http://example.com'

        # Create a mock response
        response = HtmlResponse(url=url, body=f'<html><title>{title}</title><body>{content}</body></html>')

        # Call the parse method
        parsed_data = list(self.spider.parse(response))

        # Check if the parse method yields the correct data
        self.assertEqual(len(parsed_data), 1)
        self.assertEqual(parsed_data[0]['title'], title)
        self.assertEqual(parsed_data[0]['content'], content)

        # Check if follow is called for each link
        self.assertEqual(self.spider.follow.call_count, 1)

    def test_clean_title(self):
        # Test cleaning of title with problematic characters
        title_with_problems = '<Example> Title:'
        cleaned_title = self.spider.clean_title(title_with_problems)
        self.assertEqual(cleaned_title, 'Example Title')

    def test_validate_url(self):
        # Test validation of URLs
        valid_url = 'http://example.com'
        invalid_url = 'mailto:test@example.com'
        self.assertTrue(self.spider.validate_url(valid_url))
        self.assertFalse(self.spider.validate_url(invalid_url))

if __name__ == '__main__':
    unittest.main()
