import unirest
import urllib

API_KEY = "PdrUxa0f8xmsh2QMuOV7P8ziJ9nXp1XThpMjsn9OjoBfJVEmum"
BASE_API_URL = "https://ahmedakhan-game-review-information-v1.p.mashape.com/"

def get_search_url(game_name, console):
    BASE = BASE_API_URL + "api/v1/search?"
    return BASE + urllib.urlencode({
                     #'console': console,
                     'game_name': game_name
                     })

def get_metacritic_search_result(game_name, console):
    query = get_search_url(game_name, console)
    response = unirest.get(
      query,
      headers={
        "X-Mashape-Key": API_KEY,
        "Accept": "application/json"
      }
    )
    return response.body['result']

def get_info_url(game_name, console):
    BASE = BASE_API_URL + "api/v1/information?"
    return BASE + urllib.urlencode({
                     #'console': console,
                     'game_name': game_name
                     })

def get_metacritic_result(game_name, console):
    query = get_info_url(game_name, console)
    response = unirest.get(
      query,
      headers={
        "X-Mashape-Key": API_KEY,
        "Accept": "application/json"
      }
    )
    print(response.body['result']['platform'])
    return response.body['result']['metacritic']

if __name__ == "__main__":

    print get_metacritic_search_result('call of duty black ops', 'xbox 360')