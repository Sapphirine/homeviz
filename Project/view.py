from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account
import logging
import sys
import os

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
  "private_key_id": "0cdcd493b2cc3ffaaa5fb717f5afba8605b67039",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDaBB5vjb91VW2H\n2OLq0Q2m4R+N9v/myDLoFBivQ5WBNlBojrdcIFSARISub4bE+/9xumlB2V0WVFCD\n3A6eey7k3+asuUo3um5m0bXyA1bI0CAbBivDBbDzRrILldHtgWhsUTlY1ITtYOXf\nkbGFzTv6bKbG7IYVYXXTtGOCNoPBfihYVkWo9T+v6tOQlEZ6V/jN0gV/edLr8hha\n1SZWhrOep1JR7nOtlcN0+TlyHvzXTSdAx9Sw3Zp/VWbySu7pVOPTNesYKTGpOFOl\ncr19ueaYghryG6Rzug1x1aizJxcFd3VlvFkFNanWvqpGQggFSlT+Sa3EAZl8/RJq\nyb8e+RWbAgMBAAECggEAAi3ck+6RGwUcpGZL3MkKirI8+AFRylHayO3lGmZT0fMv\nDaf4wCGpHjeIw15ftM6Qc8C2kjuZuofHQtsw6RYj/XwOfOECCFEiA9ixP/GGYhY0\nvEuLpcg7iqpE/qtNXxw3hmYqDK/L/MdXXTexkXOHCcumtJWSVwGLRXUUSD503AjT\n6E6TBVzi/1tajCK3ONkUVJXyrsVbSXRV25Pn8409bcgmf6NJmlv/kgQNtl3bGD5L\n9Eh6ZKXkUN0v5QVm7RRm6yjIyiehN7flTb5MBw6Hy521CrO2YnWYl19kMpbm20rb\nlqfpaje8Y7e7mA6clAAX09d0n2ZgT7bbPuhLpKBiuQKBgQDx0LHHJtz5nJrPaL5M\nc2X2UPN9bTxtg/SbmpV8POmYXfnV2uQDPOGte9r0nu6ui5qFH2XpLBfdlnoiNLF1\nK7JfRkukpZ82uSu4QQwe+22O1IrAMXcYLSpUf+zLBpIIzQR92zIiE1CSe0ZX1/s7\nyu8PyQSjJpYBnQ9J9BkmcI7L6QKBgQDmzglLahALh7GEFms5iGl3MA2WCZwgLk7J\nreFB99hYilaRXuLfzbVctgWgjvNHkiKl4Tli4EC6EvFiNQsKcjWhI8/3kDzDD8MC\nR6VqTP/LkE2VVOc9NQ80pUkT0OelYm+UzJXKwuxA764dG+7BWipVp94a2wxeINaQ\nIt0rospW4wKBgAWelvMM2SfH1uUpBvsZ123A9dedWUEmRuHy1rR7aeZLkMnCe3gD\nyy7P6Qe0RdGyltWvJBwmFSvmGlJ/LPyPFmcWaB2cZ7XK2dQ/VrvFlgcys0LCI4Vh\nT1GFY4hYT756nTcbh++4yS+OQ9U4xLLgBWw1fLEZ7XR+JOPQE2GMThU5AoGBANdq\nL5SablVElXLxtavh3IVobRW+7F/AuLpVNmtqlhq1KuzNAbTeesoH/SKIqRkAlKP7\nnKLjKKZCrdX6Kc7bH6DBGwY1MfDg0iJbmlCngwqMKU0aDCS9U+7P4W/ER5+9SuU3\nOQsgeH529Sun+WOu8to1LgAkt9tWjMvELmberjj/AoGAGM2Rb0DjYM0twoMg8JN6\no2gIb0AfBJUUx3u2Qc7QA5K3QYjUs44WgYV66Bv+Jz0693UxsR0Iyyaz13ZM5JAI\nybbVdvIf4AM28DKcBvjN1k9XBRl5dOEylXgjo88uGMBFIstDKFfOjfw1DbFM/vlZ\nVlugW/TsKW1yjSWhUlFECf8=\n-----END PRIVATE KEY-----\n",
  "client_email": "bigdata-admin@bigdata-253023.iam.gserviceaccount.com",
  "client_id": "101391203461485390588",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bigdata-admin%40bigdata-253023.iam.gserviceaccount.com"
}

# path = os.path.join(sys.path[0], "BigData-03aeb7de872c.json")
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# credentials = service_account.Credentials.from_service_account_file(path)

def home(request):
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "bigdata-253023"

    # SQL1 = "SELECT RegionName, _2019_09 FROM HomeViz.home_value_byState_all"
    # df1 = pandas_gbq.read_gbq(SQL1)
    # SQL2 = "SELECT RegionName, _2019_09 FROM HomeViz.home_value_byState_1bed"
    # df2 = pandas_gbq.read_gbq(SQL2)
    # SQL3 = "SELECT RegionName, _2019_09 FROM HomeViz.home_value_byState_2bed"
    # df3= pandas_gbq.read_gbq(SQL3)
    # SQL4 = "SELECT RegionName, _2019_09 FROM HomeViz.home_value_byState_3bed"
    # df4 = pandas_gbq.read_gbq(SQL4)
    # SQL5 = "SELECT RegionName, _2019_09 FROM HomeViz.home_value_byState_4bed"
    # df5 = pandas_gbq.read_gbq(SQL5)
    # SQL6 = "SELECT RegionName, _2019_09 FROM HomeViz.home_value_byState_5bedOrMore"
    # df6 = pandas_gbq.read_gbq(SQL6)
    # SQL7 = "SELECT RegionName, _2019_09 FROM HomeViz.home_value_byState_medianPerSqft"
    # df7 = pandas_gbq.read_gbq(SQL7)

    SQL1 = "SELECT * FROM HomeViz.home_value_byState_2019_09"
    df1 = pandas_gbq.read_gbq(SQL1)

    SQL2 = "SELECT * FROM HomeViz.home_value_byCounty_2019_09"
    df2 = pandas_gbq.read_gbq(SQL2)
    
    SQL3 = "SELECT * FROM HomeViz.home_value_byState_all"
    df3 = pandas_gbq.read_gbq(SQL3)

    # Convert id column (state + county code) to string and add leading zeros 
    # (to match TOPOJSON id format)
    df2['id'] = df2['id'].astype(str)
    df2['id'] = df2['id'].apply(lambda x: x.zfill(5))

    state_col_label = ["state_all", "state_1bed", "state_2bed", "state_3bed",
                "state_4bed", "state_5bed", "state_sqft"]

    county_col_label = ["county_all", "county_1bed", "county_2bed", "county_3bed",
                "county_4bed", "county_5bed", "county_sqft"]

    data = {}
    # data["state_all"] = df1.to_dict(orient='record')
    # data["state_all"] =  df1.set_index("RegionName")['_2019_09'].to_dict()
    # data["state_1bed"] =  df2.set_index("RegionName")['_2019_09'].to_dict()
    # data["state_2bed"] =  df3.set_index("RegionName")['_2019_09'].to_dict()
    # data["state_3bed"] =  df4.set_index("RegionName")['_2019_09'].to_dict()
    # data["state_4bed"] =  df5.set_index("RegionName")['_2019_09'].to_dict()
    # data["state_5bed"] =  df6.set_index("RegionName")['_2019_09'].to_dict()
    # data["state_sqft"] =  df7.set_index("RegionName")['_2019_09'].to_dict()

    # Consolidated data for heat map (state)
    for cat in state_col_label:
        data[cat] = df1.set_index("RegionName")[cat].dropna().to_dict()

    # Consolidated data for heat map (county)
    for cat in county_col_label:
        data[cat] = df2.set_index("id")[cat].dropna().to_dict()

    # Historical home value data for plots (state, all)
    # Reformat df to dict
    # Format: {state -> {column -> value}}
    data_state_all = df3.drop(columns=['RegionID', 'SizeRank']).set_index("RegionName").dropna().to_dict(orient='index')

    return render(request, 'home.html', {"data": data, "hist": data_state_all})

def test(request):
    data = {}
    return render(request, 'test.html', data)

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
