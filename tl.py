import metacritic.py



def get_games():
    URL = 'https://www.torrentleech.org/torrents/browse/index/categories/17/facets/category%253AGames_subcategory%253APC'
    response = unirest.get(URL)

if __name__ == '__main__':
    