import metacritic as mc

def find_game(title):
    results = mc.get_metacritic_search_result(title, 'PC')
    if results:
        return results[0]
    return None

def fetch_review(title):
    return mc.get_metacritic_result(title, 'PC')

if __name__ == '__main__':
    title = find_game('skyrim')
    if title:
        print(title)
        print(fetch_review(title))