import requests
import pymongo
import time
import json
import math
from loadbar import LoadBar

token = ''

bath = 100
default_quantitiy = 1000
languages = {
    'java': default_quantitiy,
    'python': default_quantitiy,
    'go': default_quantitiy,
    'c#': default_quantitiy,
    'javascript': default_quantitiy,
    'php': default_quantitiy
    }

password = 'mongodb'
username = 'mongodb'
host = 'localhost'
port = '27017'

client = pymongo.MongoClient('mongodb://%s:%s@%s:%s' % (username, password, host, port))

def run_graphql_query(url: str, query: str, variables: str, headers: dict) -> requests.Request:  
    request = requests.post(url, json={'query': query, "variables": variables}, headers=headers)
    if request.ok:
        return request
    else:
        raise Exception(requests.content)

def get_graphql_query(path: str) -> str:
    return open(path, 'r').read()


def run_pagging_graphql_query(url: str, query: str, variables: dict, headers: dict, 
        operation_name: str, total_value: int, bath_value: int):
    
    parts = math.ceil(total_value/bath_value);

    load_bar = LoadBar(30, parts);
    load_bar.init("Initalizing %d for query %s \n" % (total_value, variables['query']))

    for i in range(0, parts):
        load_bar.increase()
        
        start_time = time.time()
        result = run_graphql_query(url, query, json.dumps(variables), headers).json()
        total_time = int((time.time() - start_time) * 1000)

        variables['cursor'] = result['data'][operation_name]['pageInfo']['endCursor']
        data = list(map(lambda x: x['node'], result['data'][operation_name]['edges']))
        meta_data = {
            'number': i, 
            'query': variables['query'], 
            'time': total_time,
            'cursor':  variables['cursor']
        }

        if not result['data'][operation_name]['pageInfo']['hasNextPage']:
            meta_data['last'] = True
            yield data, meta_data;
            break;

        yield data, meta_data

def insert_mongo(data, database: str, collection: str):
    if type(data) is dict:
        client[database][collection].insert_one(data)    
    elif type(data) is list:
        client[database][collection].insert_many(data)

    
url = 'https://api.github.com/graphql'
headers = {'Authorization': 'token %s' % token}

variables = {'quantity': bath}
query = get_graphql_query('./query.graphql')

for key, value in languages.items():
    variables['query'] = "language:" + key
    
    if 'cursor' in variables:
        del variables['cursor']
    
    for data, meta_data in run_pagging_graphql_query(url, query, variables, headers, 'search', value, bath):
        insert_mongo(data, 'gitanalysis', 'gits')
        insert_mongo(meta_data, 'gitanalysis', 'metagits')
