import requests
import json

def main():
    key = open('api.key', 'r').read()
    url = 'https://api.liquipedia.net/api/v1/game'
    headers = {
        'User-Agent': 'cthorrez', 
        'accept-encoding' : 'gzip',
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    params = {
        'apikey' : key,
        'wiki' : 'counterstrike',
        'limit' : 1,
        'query' : 'opponent1, opponent2, opponent1players'
    }
    response = requests.post(url, data=params, headers=headers)
    print(response.text)
    print('\n\n')
    
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