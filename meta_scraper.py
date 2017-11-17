import urllib
import urllib2
import urlparse
from bs4 import BeautifulSoup
import functools
from contextlib import contextmanager
 
@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass

def fetch_html(url):
    # req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    # response = urllib2.urlopen(req)
    # html = response.read()
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    r = requests.get(url, headers=headers)
    return r.content

def get_soup(url):
    return BeautifulSoup(fetch_html(url), "html.parser")

def get_review_data(url):
    rd = {'mcurl': url}
    rd.update(parse_title_page(get_soup(url)))
    return rd

def parse_title_page(soup):
    d = {}
    exc = (IndexError, AttributeError)
    with ignored(exc): d['title'] = soup.find('h1', 'product_title').find('span').get_text().strip();
    with ignored(exc): d['date_pub'] = soup.find('div', 'product_data').find(itemprop='datePublished').get_text();
    with ignored(exc): d['score_review'] = soup.find('div', 'details main_details').find('div', 'metascore_w').get_text();
    with ignored(exc): d['critics'] = soup.find('div', 'summary').find(itemprop="reviewCount").get_text().strip();
    with ignored(exc): d['score_user'] = soup.find('div', 'details side_details').find_all('div', 'metascore_w')[0].get_text();
    with ignored(exc): d['ratings'] = soup.find_all('div', 'summary')[1].find('a').get_text();
    # try:
    #     d['title'] = soup.find('h1', 'product_title').find('span').get_text().strip()
    #     d['date_pub'] = soup.find('div', 'product_data').find(itemprop='datePublished').get_text()
    #     d['score_review'] = soup.find('div', 'details main_details').find('div', 'metascore_w').get_text()
    #     d['critics'] = soup.find('div', 'summary').find(itemprop="reviewCount").get_text().strip()
    #     d['score_user'] = soup.find('div', 'details side_details').find_all('div', 'metascore_w')[0].# get_text()
    #     d['ratings'] = soup.find_all('div', 'summary')[1].find('a').get_text()
    # except (IndexError, AttributeError):
    #     pass
    return d

def parse_search_page(soup, platform_filter=None):
    hits = []
    search_results = soup.find('ul', 'search_results module')
    if search_results:
        for r in search_results.find_all('li', 'result'):
            result = {}
            result['platform'] = r.find('span', 'platform').get_text()
            result['title'] = r.find('h3', 'product_title basic_stat').get_text()
            result['url'] = 'http://www.metacritic.com' + r.find('h3', 'product_title basic_stat').find('a')['href']
            hits.append(result)
    return (filter_platform_titles(hits, platform_filter) if platform_filter else hits)

def get_search_url(query):
    PRE = 'http://www.metacritic.com/search/game'
    POST = 'results'
    return '/'.join([PRE, urllib.quote_plus(query), POST])

def filter_platform_titles(hits, platform='PC'):
    return [r for r in hits if r['platform'] == platform]

def brute_search(query):
    import re
    words = re.split(' |-', query)
    searches = []
    search = ''
    for word in words:
        search = ' '.join([search, word])
        searches.append(search)
        
    for search in reversed(searches):
        url = get_search_url(search)
        #print(url)
        hits = parse_search_page(get_soup(url), platform_filter='PC')
        if hits:
            return hits
    return []

def main():
    while True:
        url = brute_search(raw_input("Search: "))
        print(url)
        print(filter_platform_titles(parse_search_page(get_soup(url))))
    
    # soup = get_soup('http://www.metacritic.com/game/pc/gears-of-war-4')
    # print(parse_title_page(soup))

if __name__ == '__main__':
    main()