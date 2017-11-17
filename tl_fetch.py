import requests

TL_BASE = 'https://www.torrentleech.org'
TL_LOGIN = '/user/account/login/'
TL_PC_GAMES_PAGE = '/torrents/browse/index/categories/17/facets/category%253AGames_subcategory%253APC/page/'

CREDENTIALS = {
    'password': 'Ju12s4ther,ro4',
    'username': 'JustAnotherBro',
}

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

class Session:
    def __init__(self):
        self.s = requests.Session()
        self.s.post(TL_BASE + TL_LOGIN, data=CREDENTIALS)
    
    def fetch_html(self, url):
        return self.s.get(url, headers=HEADERS).content

def write_html(outfile, html):
    with open(outfile, 'w') as f:
        f.write(html)

def get_pc_games_page(session, num):
    url = TL_BASE+TL_PC_GAMES_PAGE+str(num)
    return session.fetch_html(url)

def main():
    session = Session()
    html = session.fetch_html('https://www.torrentleech.org/torrents/browse/index/categories/17/facets/category%253AGames_subcategory%253APC')
    write_html('fetch.html', html)
    #import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()