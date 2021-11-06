import requests
import json

def main():
    key = open('api.key', 'r').read()
    url = 'https://api.liquipedia.net/api/v2/player'
    headers = {
        'User-Agent': 'cthorrez', 
        'accept-encoding' : 'gzip',
        'Authorization': key
    }
    params = {
        'wiki' : 'starcraft2',
        'query' : 'id, birthdate',
        'limit' : 10
    }


    response = requests.get(url, params=params, headers=headers)
    print(response)
    print(response.text)

if __name__ == '__main__':
    main()