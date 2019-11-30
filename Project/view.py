from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account
import logging
import sys
import os
import pandas as pd
import pickle
import json
import bz2
# from django.contrib.staticfiles.templatetags.staticfiles import static
# from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find

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

    state_table_prefix = "home_value_byState_"
    county_table_prefix = "home_value_byCounty_"
    tables = ["all", "1bed", "2bed", "3bed", "4bed", "5bedOrMore", "medianPerSqft",
            "singleFamily", "condo", "topTier", "bottomTier"]

    # state_col_label = ["state_all", "state_1bed", "state_2bed", "state_3bed",
    #             "state_4bed", "state_5bed", "state_sqft"]
    # county_col_label = ["county_all", "county_1bed", "county_2bed", "county_3bed",
    #             "county_4bed", "county_5bed", "county_sqft"]


    # # Save last latest data for heatmap
    # data = {}
    # hist = {}
    # for table in tables:
    #     # State data
    #     SQL = "SELECT * FROM HomeViz.home_value_byState_" + table
    #     df = pandas_gbq.read_gbq(SQL)
    #     data["state_" + table] = df.set_index('RegionName').iloc[:,-1].rename("state_" + table).dropna().to_dict()
    #     hist["state_" + table] = df.drop(columns=['RegionID', 'SizeRank']).set_index("RegionName").fillna(0).to_dict(orient='index')
        
    #     # County data
    #     SQL = "SELECT * FROM HomeViz.home_value_byCounty_" + table
    #     df = pandas_gbq.read_gbq(SQL)
    #     # Create new column "id" by concatenating "StateCodeFIPS" and "MunicipalCodeFIPS" columns
    #     df["StateCodeFIPS"] = df["StateCodeFIPS"].astype(str).apply(lambda x: x.zfill(2))
    #     df["MunicipalCodeFIPS"] = df["MunicipalCodeFIPS"].astype(str).apply(lambda x: x.zfill(3))
    #     df["id"] = df["StateCodeFIPS"] + df["MunicipalCodeFIPS"]
    #     data["county_" + table] = df.set_index('id').iloc[:,-2].rename("county_" + table).dropna().to_dict()
    #     hist["county_" + table] = df.drop(columns=['RegionID', 'RegionName', 'State', 'Metro', 'StateCodeFIPS', 'MunicipalCodeFIPS', 'SizeRank']).set_index("id").fillna(0).to_dict(orient='index')
 
    # SQL1 = "SELECT * FROM HomeViz.home_value_byState_2019_09"
    # df1 = pandas_gbq.read_gbq(SQL1)
    # SQL2 = "SELECT * FROM HomeViz.home_value_byCounty_2019_09"
    # df2 = pandas_gbq.read_gbq(SQL2)
    # SQL3 = "SELECT * FROM HomeViz.home_value_byState_all"
    # df3 = pandas_gbq.read_gbq(SQL3)
    # SQL4 = "SELECT * FROM HomeViz.home_value_byState_1bed"
    # df4 = pandas_gbq.read_gbq(SQL4)
    # SQL5 = "SELECT * FROM HomeViz.home_value_byState_2bed"
    # df5= pandas_gbq.read_gbq(SQL5)
    # SQL6 = "SELECT * FROM HomeViz.home_value_byState_3bed"
    # df6 = pandas_gbq.read_gbq(SQL6)
    # SQL7 = "SELECT * FROM HomeViz.home_value_byState_4bed"
    # df7 = pandas_gbq.read_gbq(SQL7)
    # SQL8 = "SELECT * FROM HomeViz.home_value_byState_5bedOrMore"
    # df8 = pandas_gbq.read_gbq(SQL8)
    # SQL9 = "SELECT * FROM HomeViz.home_value_byState_medianPerSqft"
    # df9 = pandas_gbq.read_gbq(SQL9)
    # SQL10 = "SELECT * FROM HomeViz.home_value_byCounty_all"
    # df10 = pandas_gbq.read_gbq(SQL10)
    # SQL11 = "SELECT * FROM HomeViz.home_value_byCounty_1bed"
    # df11 = pandas_gbq.read_gbq(SQL11)
    # SQL12 = "SELECT * FROM HomeViz.home_value_byCounty_2bed"
    # df12= pandas_gbq.read_gbq(SQL12)
    # SQL13 = "SELECT * FROM HomeViz.home_value_byCounty_3bed"
    # df13 = pandas_gbq.read_gbq(SQL13)
    # SQL14 = "SELECT * FROM HomeViz.home_value_byCounty_4bed"
    # df14 = pandas_gbq.read_gbq(SQL14)
    # SQL15 = "SELECT * FROM HomeViz.home_value_byCounty_5bedOrMore"
    # df15 = pandas_gbq.read_gbq(SQL15)
    # SQL16 = "SELECT * FROM HomeViz.home_value_byCounty_medianPerSqft"
    # df16 = pandas_gbq.read_gbq(SQL16)

    # # Convert id column (state + county code) to string and add leading zeros 
    # # (to match TOPOJSON id format)
    # df2['id'] = df2['id'].astype(str)
    # df2['id'] = df2['id'].apply(lambda x: x.zfill(5))

    # # Create new column "id" by concatenating "StateCodeFIPS" and "MunicipalCodeFIPS" columns
    # for df in county_dfs:
    #     df["StateCodeFIPS"] = df["StateCodeFIPS"].astype(str).apply(lambda x: x.zfill(2))
    #     df["MunicipalCodeFIPS"] = df["MunicipalCodeFIPS"].astype(str).apply(lambda x: x.zfill(3))
    #     df["id"] = df["StateCodeFIPS"] + df["MunicipalCodeFIPS"]

    # df1.to_pickle("./static/df1,pkl")
    # df2.to_pickle("./static/df2,pkl")
    # df3.to_pickle("./static/df3,pkl")
    # df4.to_pickle("./static/df4,pkl")
    # df5.to_pickle("./static/df5,pkl")
    # df6.to_pickle("./static/df6,pkl")
    # df7.to_pickle("./static/df7,pkl")
    # df8.to_pickle("./static/df8,pkl")
    # df9.to_pickle("./static/df9,pkl")
    # df10.to_pickle("./static/df10.pkl")
    # df11.to_pickle("./static/df11.pkl")
    # df12.to_pickle("./static/df12.pkl")
    # df13.to_pickle("./static/df13.pkl")
    # df14.to_pickle("./static/df14.pkl")
    # df15.to_pickle("./static/df15.pkl")
    # df16.to_pickle("./static/df16.pkl")

    # df1 = pd.read_pickle(static("df1.pkl"))
    # df2 = pd.read_pickle(static("df2.pkl"))
    # df3 = pd.read_pickle(static("df3.pkl"))
    # df4 = pd.read_pickle(static("df4.pkl"))
    # df5 = pd.read_pickle(static("df5.pkl"))
    # df6 = pd.read_pickle(static("df6.pkl"))
    # df7 = pd.read_pickle(static("df7.pkl"))
    # df8 = pd.read_pickle(static("df8.pkl"))
    # df9 = pd.read_pickle(static("df9.pkl"))
    # df10.to_pickle("./static/df10.pkl")
    # df11.to_pickle("./static/df11.pkl")
    # df12.to_pickle("./static/df12.pkl")
    # df13.to_pickle("./static/df13.pkl")
    # df14.to_pickle("./static/df14.pkl")
    # df15.to_pickle("./static/df15.pkl")
    # df16.to_pickle("./static/df16.pkl")

    # df1 = pd.read_pickle(find("df1.pkl"))
    # df2 = pd.read_pickle(find("df2.pkl"))
    # df3 = pd.read_pickle(find("df3.pkl"))
    # df4 = pd.read_pickle(find("df4.pkl"))
    # df5 = pd.read_pickle(find("df5.pkl"))
    # df6 = pd.read_pickle(find("df6.pkl"))
    # df7 = pd.read_pickle(find("df7.pkl"))
    # df8 = pd.read_pickle(find("df8.pkl"))
    # df9 = pd.read_pickle(find("df9.pkl"))
    # df10 = pd.read_pickle(find("df10.pkl"))
    # df11 = pd.read_pickle(find("df11.pkl"))
    # df12 = pd.read_pickle(find("df12.pkl"))
    # df13 = pd.read_pickle(find("df13.pkl"))
    # df14 = pd.read_pickle(find("df14.pkl"))
    # df15 = pd.read_pickle(find("df15.pkl"))
    # df16 = pd.read_pickle(find("df16.pkl"))

    # state_dfs = [df3, df4, df5, df6, df7, df8, df9]
    # county_dfs = [df10, df11, df12, df13, df14, df15, df16]

    # data = {}

    # # Consolidated data for heat map (state)
    # for cat in state_col_label:
    #     data[cat] = df1.set_index("RegionName")[cat].dropna().to_dict()

    # # Consolidated data for heat map (county)
    # for cat in county_col_label:
    #     data[cat] = df2.set_index("id")[cat].dropna().to_dict()

    # # Historical home value data for plots (state, all)
    # # Reformat df to dict
    # # Format: {category --> {state/county -> {column -> value}}}
    # hist = {}
    # for i, cat in enumerate(state_col_label):
    #     hist[cat] = state_dfs[i].drop(columns=['RegionID', 'SizeRank']).set_index("RegionName").fillna(0).to_dict(orient='index')

    # for i, cat in enumerate(county_col_label):
    #     hist[cat] = county_dfs[i].drop(columns=['RegionID', 'RegionName', 'State', 'Metro', 'StateCodeFIPS', 'MunicipalCodeFIPS', 'SizeRank']).set_index("id").fillna(0).to_dict(orient='index')

    # # Cache files
    # with open("./static/data.pkl", "wb") as handle:
    #     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # with open("./static/hist.pkl", "wb") as handle:
    #     pickle.dump(hist, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # # Retrieve Cache files
    # with open(find("data.pkl"), "rb") as handle:
    #     data = pickle.load(handle)
    # with open(find("hist.pkl"), "rb") as handle:
    #     hist = pickle.load(handle)

    # # Cache JSON files
    # with open("./static/data.txt", "w") as handle:
    #     json.dump(data, handle)
    # with open("./static/hist.txt", "w") as handle:
    #     json.dump(hist, handle)

    # # Retrieve Cache JSON files
    # with open(find("data.txt"), "r") as handle:
    #     data = json.load(handle)
    # with open(find("hist.txt"), "r") as handle:
    #     hist = json.load(handle)

    # Dump for saving files
    data_file = bz2.BZ2File(find('data.s'), 'r')
    data = pickle.load(data_file)
    hist_file = bz2.BZ2File(find('hist.s'), 'r')
    hist = pickle.load(hist_file)

    return render(request, 'home.html', {"data": data, "hist": hist})

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
