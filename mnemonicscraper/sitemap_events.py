import requests
from bs4 import BeautifulSoup
import hashlib
import os
import time
from rich import print


def compare_sitemaps(sitemap_url, storage_file="previous_sitemap.xml"):
    # Fetch the current sitemap
    response = requests.get(sitemap_url)
    current_soup = BeautifulSoup(response.content, 'xml')

    # Load the previous sitemap (if it exists)
    try:
        with open(storage_file, "r") as f:
            previous_soup = BeautifulSoup(f.read(), 'xml')
    except FileNotFoundError:
        previous_soup = None

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

    return changed_urls 

if __name__ == "__main__":
    SITE_MAP_URL = "https://www.mnemonic.io/sitemap.xml"

    while True:

        changed_urls = compare_sitemaps(SITE_MAP_URL)

        for change_type, url_tag in changed_urls:
            loc = url_tag.find('loc').text
            lastmod = url_tag.find('lastmod').text
            print(f"Change Type: {change_type}, URL: {loc}, Last Modified: {lastmod}") 

        time.sleep(120)  # Check every minute
        print("next check...")


