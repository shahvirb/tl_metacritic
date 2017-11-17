from bs4 import BeautifulSoup
import scene_strip as ss
from tl_parse import *

TL_BASE = 'https://www.torrentleech.org'

def get_soup(file_path):
    return BeautifulSoup(open(file_path), "html.parser")

if __name__ == '__main__':
    soup = get_soup("test.html")
    titles = parse_torrent_titles(soup)
    for t in titles:
        print(ss.strip_title(t))