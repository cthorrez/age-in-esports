import requests
import json
import pickle
import gzip
import os
import time
from copy import deepcopy
import pandas as pd

class LPDBCache():
    """
    A class to handle querying from LPDB via the API. This persists queries and results to disk.
    If a query has been made before, it retrieves it from cache rather than from the API
    """
    def __init__(self, timeout=10, limit=1000):
        self.root_url = 'https://api.liquipedia.net/api/'
        self.key = open('api.key', 'r').read()
        self.headers = {'accept-encoding' : 'gzip'}
        self.timeout = timeout
        self.limit = limit
        self.path = 'cache.gz'
        if os.path.exists(self.path):
            self.data = pickle.load(gzip.open(self.path, 'rb'))
            self.data_modified = False
        else:
            self.data = {}
            self.data_modified = True

    def get(self, query, force_refresh=False, offset=0):
        endpoint = query['endpoint']
        del query['endpoint']
        version = query['version']
        del query['version']
        done=False
        results = []
        while not done:
            batch_results = self.get_batch(version, endpoint, query, offset, force_refresh)
            results.extend(batch_results)
            offset += len(batch_results)
            if len(batch_results) < self.limit:
                done = True
            # if len(results) > 25000:
            #     done = True
        return results
        
    def get_batch(self, version, endpoint, query, offset, force_refresh=False):
        query['offset'] = offset
        query['limit'] = self.limit
        key = str(query)
        if key in self.data and not force_refresh:
            print('getting result from cache')
            print(key)
            return self.data[key]
        url = self.root_url + version + '/' + endpoint
        print('getting result from api')
        print(key)
        time.sleep(self.timeout)
        headers = deepcopy(self.headers)
        if version == 'v1':
            batch_query = deepcopy(query)
            batch_query['apikey'] = self.key
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            response = requests.post(url, data=batch_query, headers=headers)
        elif version == 'v2':
            headers['authorization'] = 'Apikey ' + self.key
            response = requests.get(url, params=query, headers=headers)
        response = json.loads(response.text)
        if 'error' in response:
            print(response)
        result = response['result']
        # print(result)
        self.data[key] = result
        self.data_modified = True
        return result

    def write(self):
        outfile = gzip.open(self.path, 'wb')
        pickle.dump(self.data, outfile)
        outfile.close()


    def __del__(self):
        if self.data_modified:
            self.write()

if __name__ == '__main__':
    cache = LPDBCache(timeout=1, limit=1000)
    query = {
        'endpoint' : 'player',
        'wiki' : 'starcraft2',
        'query' : 'id, birthdate'
    }
    players = cache.get(query)
    players = pd.DataFrame(players)
    # players = players[players['birthdate'] != '1970-01-01']
    print(players)
    print(len(players))
    del(cache)

            




