import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import sys
import threading

visited_urls = set()
base_url = 'http://www.doge24190.top'
total_urls_to_crawl = 0
is_crawling = True

def print_ellipsis():
    ellipsis_count = 0
    while is_crawling:
        print('\r' + ' ' * 20, end='', flush=True)  # 清除当前行
        ellipsis = '.' * ellipsis_count
        print(f"\r正在爬取中{ellipsis}", end='', flush=True)
        ellipsis_count = (ellipsis_count + 1) % 4
        time.sleep(1)

def is_valid_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != urlparse(base_url).netloc:
        return False
    return True

def should_print_url(url):
    parsed_url = urlparse(url)
    return not parsed_url.query and not parsed_url.fragment

def get_all_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            if is_valid_url(link):
                links.add(link)
        return links
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching {url}: {e}")
        return set()

def crawl(url):
    global total_urls_to_crawl
    if url in visited_urls:
        return
    visited_urls.add(url)
    total_urls_to_crawl += 1

    if should_print_url(url):
        print('\r' + ' ' * 20, end='', flush=True)  # 清除当前行
        print(f'URL: {url}')
    
    links = get_all_links(url)
    for link in links:
        crawl(link)
        time.sleep(1)

def main():
    global is_crawling
    try:
        threading.Thread(target=print_ellipsis, daemon=True).start()
        crawl(base_url)
        print(f"\n已爬取完成，共爬取了 {total_urls_to_crawl} 个 URL")
    except KeyboardInterrupt:
        is_crawling = False
        print("\n爬虫已停止")
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n程序已停止")
                break

if __name__ == '__main__':
    main()