import requests
import json

def main():
    key = open('api.key', 'r').read()
    url = 'https://api.liquipedia.net/api/v1/match'
    headers = {
        'User-Agent': 'cthorrez', 
        'accept-encoding' : 'gzip',
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    params = {
        'apikey' : key,
        'wiki' : 'rainbowsix',
        'limit' : 100,
        'offset' : 0,
        'query' : 'date, opponent1, opponent2, opponent1score, opponent2score, opponent1players, opponent2players, ' + \
                  'mode, type, game, matchid, pageid, pagename, objectname, extradata',
        'conditions' : '[[date::!1970-01-01]] AND [[date::!1000-01-01]] AND [[walkover::!1]] AND [[walkover::!2]] AND [[pagename::Ascension_League/2/Season_1/A]] AND [[date::2020-07-20 18:00:00]]',
        'order' : 'date ASC'
    }
    response = requests.post(url, data=params, headers=headers)
    print(response.text)
    print('\n\n')

    for row in json.loads(response.text)['result']:
        print(row)
    
    exit(1)


    url = 'https://api.liquipedia.net/api/v2/player'
    headers = {
        'User-Agent': 'cthorrez', 
        'accept-encoding' : 'gzip',
        'authorization' : 'Apikey ' + key
    }
    params = {
        'wiki' : 'warcraft',
        'limit' : 1,
        'offset' : 0,
        'order' : 'id ASC',
        'query' : 'id, alternateid, birthdate, nationality, status, earnings'
    }
    response = requests.get(url, params=params, headers=headers)
    print(response)
    print(response.request.__dict__)
    print(response.text, type(response.text), response.text=='')

if __name__ == '__main__':
    main()