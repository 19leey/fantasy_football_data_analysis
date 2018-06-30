from datetime import datetime
from tqdm import tqdm
import pandas as pd
import numpy as np


# constants
undesireable_cols = ['PPR', 'DKPt', 'FDPt', 'VBD', 'OvRank']


# web scrape fantasy player ranking data for season year
# source: https://www.pro-football-reference.com
def get_data(year):
    print('Getting year %d data' % year)
    url = 'https://www.pro-football-reference.com/years/' + str(year) + '/fantasy.htm#fantasy::none'
    df = pd.read_html(url, skiprows=1, header=0)[0]
    df = df.drop(undesireable_cols, axis=1)
    df = df.rename({'Unnamed: 1' : 'Name'}, axis='columns')
    df['Year'] = year
    return df


# convert data frame columns to correct data type
def convert_collection_dtype(data_frame):
    df = data_frame
    for col in df:
        if col not in ['Name', 'Tm', 'FantPos']:
            df[col] = pd.to_numeric(df[col])
    return df


# create collection of fantasy data - last 5 seasons
def create_collection():
    print('Creating data collection')
    df = pd.DataFrame()
    curr_year = datetime.now().year

    # for ease of testing
    df = df.append(get_data(2017), ignore_index=True)

    #for year in range((curr_year - 5), curr_year):
    #    df = df.append(get_data(str(year)), ignore_index=True)
    df = df[df.Rk != 'Rk']
    df = convert_collection_dtype(df)
    return df


# parse the collection by fantasy position
def parse_by_position(data_frame):
    print('Parsing data by position')
    df = data_frame
    qb_df = pd.DataFrame()
    rb_df = pd.DataFrame()
    wr_df = pd.DataFrame()
    te_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['FantPos'] == 'QB':
            qb_df = qb_df.append(row, ignore_index=True)
        elif row['FantPos'] == 'RB':
            rb_df = rb_df.append(row, ignore_index=True)
        elif row['FantPos'] == 'WR':
            wr_df = wr_df.append(row, ignore_index=True)
        elif row['FantPos'] == 'TE':
            te_df = te_df.append(row, ignore_index=True)

    print('Cleaning data frame columns')
    qb_df = qb_df.drop(['Att.1', 'Yds.1', 'Y/A', 'TD.1', 'Tgt', 'Rec', 'Yds.2', 'Y/R', 'TD.2'], axis=1)
    rb_df = rb_df.drop(['Cmp', 'Att', 'Yds', 'TD', 'Int', 'Tgt', 'Rec', 'Yds.2', 'Y/R', 'TD.2'], axis=1)
    wr_df = wr_df.drop(['Cmp', 'Att', 'Yds', 'TD', 'Int', 'Att.1', 'Yds.1', 'Y/A', 'TD.1'], axis=1)
    te_df = te_df.drop(['Cmp', 'Att', 'Yds', 'TD', 'Int', 'Att.1', 'Yds.1', 'Y/A', 'TD.1'], axis=1)

    dfs = {'QB' : qb_df, 'RB' : rb_df, 'WR' : wr_df, 'TE' : te_df}
    return dfs




# call the functions
df = create_collection()
dfs = parse_by_position(df)
