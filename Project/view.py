from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account
import logging
import sys
import os
from google.cloud import storage

logger = logging.getLogger(__name__)

# Make sure you have installed pandas-gbq at first;
# You can use the other way to query BigQuery.
# please have a look at
# https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
# To get your credential

# client = storage.Client()
# bucket = client.get_bucket("big_data_es")
# blob = bucket.get_blob("gs://big_data_es/HomeViz/BigData-03aeb7de872c.json")
# service_account_info = blob.download_as_string()

service_account_info = {
  "type": "service_account",
  "project_id": "bigdata-253023",
  "private_key_id": "03aeb7de872c1c1725ab46764fecaadbd0068d5d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDNg11JCqKmMRwr\nBffn4brWRVWE3et7a1mE1QrEvx/HSiHJQ5+3DttJxvvfiJP7a/MdxZX5rO+zTxVw\nz4SgcTZxce2YrearHh4/vQHtxe62R1ZQws6viiXeRp9JOrwCVINztLdb0RoJHPM6\nDoZIV0YTBwpmeL1lyxkwycAkCDJm9lbM9UNkHOK16DN9MppAFbs21wsCqcMwdcV5\nPkcYnlBWe+MftnLQl64HU33E3XO8F3kgi+8QL3d+VAEVXC/K6+yJWg1B/RpYYchC\nUNyP3ceX4Y/Ga5idL5YEk6Q7RsZHX+ycu0nGv3UisIrTQsxRPJo1JD4/69DbzKFd\nlTSXjv1bAgMBAAECggEADfVHSjU14SoXuteqbpjhwDja+0MOrIYY1pFDrHjmAc/y\npdajy+KZ7pOxurfDg+w2icXy5Dokg54Hm5m0l9MTUAwysiUpiWNqdDN0Tz/GG/eS\nELp9IDthTAypjTyMgBoDsuxKFysyD1QPNFkVMhJKDkkdoeJpzAv0d4r/CP4iMjpC\nIf0Wlh84MlSTcd3oI9fe6is93W/LVMjIYn6hsKV1lOoh2ecLNe5Px35Vmu5QljvO\necm/lcR4waxxQAB27hvGIswb0d7RDAAzhdFBr6xLTh+WhezzpGgmKvqL8Tvhp7bF\nECZpD9X1uKb/dnFxR/68kvqFN3pBF2QI8ZGTGdczdQKBgQDo/yUXK1ucpQC/RMn9\nauTZRu76N4six253ijeuthZby5IQlQLLgOS95MRxMum+SFrERmYfSV5IF1iz9O5b\nw66qfQSGB9jkjQ3X+p3vauhDxF9KPLuaQxf8KLktcOtPosr+udtT1llK5sY2Rrhq\nhmqwhHMafONIaHwQ7KIzgFZE1wKBgQDhzZbu8tvsF/jdVpejglLboKnrvDbwb2MC\nP/IUzF2X5/AdSZzX2Bvlksn0tzma8gXNk8lsnRt7I3gW+MfXCyNwlOnWhQP6leTD\nvDRIUO3KUCo19es37jqc0DkxR4jvEdUAgYHAdPwH8LRZAneDsLBZm5RJIsZmDxTY\ns0oZFBk3HQKBgAH72ib+WYNV7FG0ljuwI06uSe6bdnXPWONvq9Wy+zHA4/d8LU/q\nQwhS4FFOa6sRFqTBLLFrgIAAouK1XSou2lfdRKKXgoM/qDSEj7+wG1YoX99T8Qz5\nMUUWW61FXtuIuU29614lXxFCMcHYjE1r45CpMAmzsoO1UAkc2qyxlQp1AoGAbFr0\n19twz329bbF0+QC79CrH/5iFIKHC+DxpVbOwIgop/lPp0OYilOr4wNb/7KvBPyJx\nIQ7PNisSIKvncfklW4wKHmgcPa6aZZc125ICWfhYGSbWZjOKqt984nn6awa6mRCM\njCdXHhRS5ve5FFfAeG+hG+t1G1qXXVnD7/7mDr0CgYAR2ryreP3hQXo3F8apYN1D\nhFbqTdXGT3nqtWnTTlWlN3xxDHjLf13ph/OjMhwAIWox0eFI/UOpmBWL5J0G4sOe\n9MnJYmRF2vDVz33JdkVW8umWjShsa5lNgMr7ydFoE4Jq3opkE4ZB83yRoNLAMjLA\nhViFvYVMxAnBzwGBn2faIA==\n-----END PRIVATE KEY-----\n",
  "client_email": "bigdata-admin@bigdata-253023.iam.gserviceaccount.com",
  "client_id": "101391203461485390588",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bigdata-admin%40bigdata-253023.iam.gserviceaccount.com"
}

# path = os.path.join(sys.path[0], "BigData-03aeb7de872c.json")
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# credentials = service_account.Credentials.from_service_account_file("/Users/Enoch/Downloads/BigData-03aeb7de872c.json")

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
