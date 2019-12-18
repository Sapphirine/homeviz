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
from django.contrib.staticfiles.finders import find

# client = storage.Client()
# bucket = client.get_bucket("big_data_es")
# blob = bucket.get_blob("gs://big_data_es/HomeViz/BigData-03aeb7de872c.json")
# service_account_info = blob.download_as_string()

# service_account_info = {} 

def home(request):
    # pandas_gbq.context.credentials = credentials
    # pandas_gbq.context.project = "bigdata-253023"

    state_table_prefix = "home_value_byState_"
    county_table_prefix = "home_value_byCounty_"
    tables = ["all", "singleFamily", "condo", "topTier", "bottomTier"]

    # # Query and save data as dataframes
    # data = {}
    # hist = {}
    #  # Query data from BigQuery and cache into pickles
    # for i, table in enumerate(tables):
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
    
    # # Query data from BigQuery and cache into pickles
    # for i, table in enumerate(tables):
    #     # State data
    #     SQL = "SELECT * FROM HomeViz.home_value_byState_" + table
    #     df = pandas_gbq.read_gbq(SQL)
    #     df.to_pickle("./static/dfs{}.pkl".format(i))
        
    #     # County data
    #     SQL = "SELECT * FROM HomeViz.home_value_byCounty_" + table
    #     df = pandas_gbq.read_gbq(SQL)
    #     # Create new column "id" by concatenating "StateCodeFIPS" and "MunicipalCodeFIPS" columns
    #     df["StateCodeFIPS"] = df["StateCodeFIPS"].astype(str).apply(lambda x: x.zfill(2))
    #     df["MunicipalCodeFIPS"] = df["MunicipalCodeFIPS"].astype(str).apply(lambda x: x.zfill(3))
    #     df["id"] = df["StateCodeFIPS"] + df["MunicipalCodeFIPS"]
    #     df.to_pickle("./static/dfc{}.pkl".format(i))
        
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

    # income = {}
    # # Get income data
    # SQL = "SELECT FIPS, Area_name, Median_Household_income_2017 AS income, Unemployment_rate_2018 AS unemployment FROM HomeViz.income"
    # df = pandas_gbq.read_gbq(SQL)
    # df["FIPS"] = df["FIPS"].astype(str).apply(lambda x: x.zfill(5))
    # income['income'] = df.set_index('FIPS')['income'].dropna().to_dict()
    # income['unemployment'] = df.set_index('FIPS')['unemployment'].dropna().to_dict()
    # with open("./static/income.pkl", "wb") as handle:
    #     pickle.dump(income, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # summary = {}
    # # Get income data
    # SQL = "SELECT * FROM HomeViz.home_value_byState_summaryAll"
    # df = pandas_gbq.read_gbq(SQL)
    # summary['state'] = df.set_index('RegionName').drop(columns=['Date', 'RegionID']).dropna().to_dict(orient='index')
    # SQL = "SELECT index.id, summary.state, summary.SizeRank, summary.zhvi, summary.MoM, summary.QoQ, summary.YoY, summary._5Year, summary._10Year, summary.PeakMonth, summary.PeakQuarter, summary.PeakZHVI, summary.PctFallFromPeak, summary.LastTimeAtCurrZHVI FROM HomeViz.home_value_byCounty_summaryAll AS summary JOIN HomeViz.county_index as index ON summary.RegionID = index.RegionID and summary.state = index.state"
    # df = pandas_gbq.read_gbq(SQL)
    # df["id"] = df["id"].astype(str).apply(lambda x: x.zfill(5))
    # summary['county'] = df.set_index('id').dropna().to_dict(orient='index')
    # with open("./static/summary.pkl", "wb") as handle:
    #     pickle.dump(summary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Retrieve Cache files
    with open(find("data.pkl"), "rb") as handle:
        data = pickle.load(handle)
    with open(find("hist.pkl"), "rb") as handle:
        hist = pickle.load(handle)
    with open(find("income.pkl"), "rb") as handle:
        income = pickle.load(handle)
    with open(find("summary.pkl"), "rb") as handle:
        summary = pickle.load(handle)


    return render(request, 'home.html', {"data": data, "hist": hist, "income": income, "summary": summary})
