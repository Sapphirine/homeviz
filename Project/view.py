from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account
import logging
import os
import sys

logger = logging.getLogger(__name__)

# storage_client = gcs.Client()
# bucket = storage_client.get_bucket("big_data_es")
# file = storage_client.open("big_data_es/HomeViz/BigData-03aeb7de872c.json")

# Make sure you have installed pandas-gbq at first;
# You can use the other way to query BigQuery.
# please have a look at
# https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
# To get your credential

# credentials = service_account.Credentials.from_service_account_file("/Users/Enoch/Downloads/BigData-03aeb7de872c.json")
path = os.path.join(sys.path[0], "BigData-03aeb7de872c.json")
credentials = service_account.Credentials.from_service_account_file(path)

def map(request):
    data = {}
    return (request, 'map.html', data)

def hello(request):
    context = {}
    context['content1'] = 'Hello World!'
    return render(request, 'helloworld.html', context)


def dashboard(request):
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "bigdata-253023"

    SQL = "SELECT * FROM hw4.wordcount_byTime ORDER BY time ASC LIMIT 8" 
    df = pandas_gbq.read_gbq(SQL)

    data = {}
    data['data'] = []
    labels = ['ai', 'data', 'good', 'movie', 'spark']
    debug = []

    for i in df.index:
        temp = {}
        time = df['Time'][i].split(' ')[0].split(':')
        time = time[0] + ':' + time[1]
        temp['Time'] = time
        temp['count'] = {}
        for label in labels:
            temp['count'][label] = df[label][i]
        data['data'].append(temp)
    '''
        TODO: Finish the SQL to query the data, it should be limited to 8 rows. 
        Then process them to format below:
        Format of data:
        {'data': [{'Time': hour:min, 'count': {'ai': xxx, 'data': xxx, 'good': xxx, 'movie': xxx, 'spark': xxx}},
                  {'Time': hour:min, 'count': {'ai': xxx, 'data': xxx, 'good': xxx, 'movie': xxx, 'spark': xxx}},
                  ...
                  ]
        }
    '''

    return render(request, 'dashboard.html', data)


def connection(request):
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "bigdata-253023"
    SQL1 = 'SELECT * FROM hw4.nodes ORDER BY node ASC'
    df1 = pandas_gbq.read_gbq(SQL1)

    SQL2 = 'SELECT * FROM hw4.edges ORDER BY source ASC'
    df2 = pandas_gbq.read_gbq(SQL2)

    data = {}

    data['n'] = df1.to_dict(orient='record')
    data['e'] = df2.drop_duplicates().to_dict(orient='record')

    '''
        TODO: Finish the SQL to query the data, it should be limited to 8 rows. 
        Then process them to format below:
        Format of data:
        {'n': [xxx, xxx, xxx, xxx],
         'e': [{'source': xxx, 'target': xxx},
                {'source': xxx, 'target': xxx},
                ...
                ]
        }
    '''
    return render(request, 'connection.html', data)

    # edges = []
    # data['n'] = []
    # data['e'] = []

    # for i in df1.index:
    #     data['n'].append({'node': df1['node'][i]})

    # for i in df2.index:
    #     temp = {}
    #     temp['source'] = df2['source'][i]
    #     temp['target'] = df2['target'][i] 
    #     if not [temp['source'], temp['target']] in edges:
    #         data["e"].append(temp)
    #     edges.append([temp['source'], temp['target']])
