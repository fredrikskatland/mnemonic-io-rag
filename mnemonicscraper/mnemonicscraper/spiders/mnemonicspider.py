from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
import xml.etree.ElementTree as ET
from mnemonicscraper.items import MnemonicscraperItem
from scrapy.loader import ItemLoader

import requests
from bs4 import BeautifulSoup
import hashlib
import os
import time
from rich import print

def compare_sitemaps(sitemap_url, storage_file="previous_sitemap.xml", retries=0, max_retries=3):
    if retries > max_retries:
        print("Max retries reached")
        return 
    
    # Fetch the current sitemap
    response = requests.get(sitemap_url)
    current_soup = BeautifulSoup(response.content, 'xml')

    # Load the previous sitemap (if it exists), otherwise write the current sitemap to the storage file, increment retries and call the function again
    try:
        # Check if file exists
        if os.path.exists(storage_file):
            #print(f"File exists: {storage_file}")
            with open(storage_file, "r") as f:
                previous_soup = BeautifulSoup(f.read(), 'xml')
        else:
            # File does not exist, create the file
            print(f"Creating file: {storage_file}")
            with open(storage_file, 'w') as file:
                file.write("This is a new file.")
            # Call the function again to check if the file now exists
            compare_sitemaps(sitemap_url, storage_file, retries=retries+1, max_retries=max_retries)
            with open(storage_file, "r") as f:
                previous_soup = BeautifulSoup(f.read(), 'xml')
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, you can attempt to retry here as well
        compare_sitemaps(sitemap_url, storage_file, retries=retries+1, max_retries=max_retries)
        with open(storage_file, "r") as f:
            previous_soup = BeautifulSoup(f.read(), 'xml')


    # Compare for changes
    changed_urls = []
    if previous_soup:
        current_hashes = set(hashlib.md5(url_tag.encode()).hexdigest() for url_tag in current_soup.find_all('url'))
        previous_hashes = set(hashlib.md5(url_tag.encode()).hexdigest() for url_tag in previous_soup.find_all('url'))

        new_urls = current_hashes - previous_hashes
        removed_urls = previous_hashes - current_hashes

        for url_tag in current_soup.find_all('url'):
            url_hash = hashlib.md5(url_tag.encode()).hexdigest()
            if url_hash in new_urls:
                changed_urls.append(("new", url_tag))
            elif url_hash in removed_urls:
                changed_urls.append(("removed", url_tag))
            elif url_tag.find('lastmod'):  # Check if <lastmod> exists in the current tag
                url_match = previous_soup.find('url', loc=url_tag.find('loc').text)
                if url_match and url_match.find('lastmod'):  # Check if match and <lastmod> exist
                    if url_tag.find('lastmod').text != url_match.find('lastmod').text:
                        changed_urls.append(("modified", url_tag))

    # Store the current sitemap as the new "previous"
    with open(storage_file, "w") as f:
        f.write(response.content.decode())  

    #print("Changed URLs: ", changed_urls)
    return changed_urls 

def extract_product_links(sitemap_url):
    # Send a GET request to the sitemap URL
    response = requests.get(sitemap_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve the sitemap")
        return []

    # Parse the XML content
    root = ET.fromstring(response.content)

    # Extract URLs
    solutions_links = []
    for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        if 'www.mnemonic.io' in loc:
            solutions_links.append(loc)

    return solutions_links

sitemap_url = 'https://www.mnemonic.io/sitemap.xml'
#solutions_links = extract_product_links(sitemap_url)
solution_links = compare_sitemaps(sitemap_url, storage_file="../previous_sitemap.xml", retries=0, max_retries=3)
unique_product_links = list(set(solution_links))

class MnemonicSpider(scrapy.Spider):
    name = "mnemonicspider"
    start_urls = unique_product_links

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,  # Timeout in seconds
    }

    def parse(self, response):
        
        url_split = response.url.split('/')
        
        item = MnemonicscraperItem()

        l = ItemLoader(item=MnemonicscraperItem(), selector=response)
        l.add_css("title", 'h1')
        l.add_css("ingress", 'p')
        l.add_css("content", 'div.xhtml p')
        l.add_value("url", response.url)
        l.add_value("category", url_split[3])
        l.add_value("subcategory", url_split[4] if len(url_split) > 4 else '')
        
        yield l.load_item()
