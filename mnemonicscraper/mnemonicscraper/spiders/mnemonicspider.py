from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
import xml.etree.ElementTree as ET

def extract_product_links(sitemap_url):
    # Send a GET request to the sitemap URL
    response = requests.get(sitemap_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve the sitemap")
        return []

    # Parse the XML content
    root = ET.fromstring(response.content)

    # Extract URLs containing 'brewshop.no/produkt'
    solutions_links = []
    for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        if 'www.mnemonic.io' in loc:
            solutions_links.append(loc)

    return solutions_links

sitemap_url = 'https://www.mnemonic.io/sitemap.xml'
solutions_links = extract_product_links(sitemap_url)
unique_product_links = list(set(solutions_links))

class MnemonicSpider(scrapy.Spider):
    name = "mnemonicspider"
    start_urls = unique_product_links

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,  # Timeout in seconds
    }

    def parse(self, response):
       title = response.css('h1::text').get().strip()
       ingress = response.css('p::text').get().strip()
       content = response.css('div.xhtml p::text').getall()
       content_text = ''.join(content).strip()

       url_split = response.url.split('/')

       yield {
            'title': title,
            'ingress': ingress,
            'content': content_text,
            'url': response.url,
            'category': url_split[3],
            'subcategory': url_split[4] if len(url_split) > 4 else ''
        }
