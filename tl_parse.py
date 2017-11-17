from bs4 import BeautifulSoup

TL_BASE = 'https://www.torrentleech.org'

def make_html_soup(html):
    return BeautifulSoup(html, "html.parser")

def tl_absolute(relative):
    return TL_BASE + relative

def parse_torrent_titles(soup):
    titles = []
    for torrent in soup.find_all('td', 'name'):
        titles.append({
                      'title': torrent.find('span', 'title').contents[0].text.encode('ascii',errors='ignore'),
                      'url': tl_absolute(torrent.find('span', 'title').contents[0]['href'])
                      })
    return titles