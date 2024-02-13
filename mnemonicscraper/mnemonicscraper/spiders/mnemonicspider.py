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
        if 'www.mnemonic.io/solutions' in loc:
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
       solution_description = response.css('div.xhtml p::text').getall()
       solution_description_text = ''.join(solution_description).strip()

       yield {
            'solution_description': solution_description_text,
            'url': response.url,
        }
