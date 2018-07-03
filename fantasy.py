from datetime import datetime
from tqdm import tqdm
import pandas as pd
import numpy as np


# constants
undesireable_cols = ['PPR', 'DKPt', 'FDPt', 'VBD', 'OvRank']
non_qb_cols = ['Att.1', 'Yds.1', 'Y/A', 'TD.1', 'Tgt', 'Rec', 'Yds.2', 'Y/R', 'TD.2']
non_rb_cols = ['Cmp', 'Att', 'Yds', 'TD', 'Int', 'Tgt', 'Rec', 'Yds.2', 'Y/R', 'TD.2']
non_wr_cols = ['Cmp', 'Att', 'Yds', 'TD', 'Int', 'Att.1', 'Yds.1', 'Y/A', 'TD.1']

years = []


# web scrape fantasy player ranking data for season year
# source: https://www.pro-football-reference.com
def get_data(year):
    print('Getting year %s data' % year)
    url = 'https://www.pro-football-reference.com/years/' + year + '/fantasy.htm#fantasy::none'
    df = pd.read_html(url, skiprows=1, header=0)[0]
    df = df.drop(undesireable_cols, axis=1)
    df = df.rename({'Unnamed: 1' : 'Name'}, axis='columns')
    df.to_csv(('output/%s_season.csv' % year), index=False)
    df['Year'] = year
    return df


# convert data frame columns to correct data typef
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
    for year in range((curr_year - 5), curr_year):
        df = df.append(get_data(str(year)), ignore_index=True)
        years.append(year)
    df = df[df.Rk != 'Rk']
    df = convert_collection_dtype(df)
    df.to_csv('output/past_seasons_collection.csv', index=False)
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
    qb_df = qb_df.drop(non_qb_cols, axis=1)
    rb_df = rb_df.drop(non_rb_cols, axis=1)
    wr_df = wr_df.drop(non_wr_cols, axis=1)
    te_df = te_df.drop(non_wr_cols, axis=1)

    dfs = {'QB' : qb_df, 'RB' : rb_df, 'WR' : wr_df, 'TE' : te_df}
    return dfs


def create_position_csv(data_frame):
    dfs = parse_by_position(df)
    for pos in dfs:
        dfs[pos].to_csv(('output/%s_data.csv' % pos.lower()), index=False)


# Aaron Rodgers - https://www.pro-football-reference.com/players/R/RodgAa00.htm
# https://www.pro-football-reference.com/players/R/RodgAa00/fantasy/--year--/

# parse the collection by player name
def parse_by_player(data_frame, player_name):
    print('Parsing data by player name: %s' % player_name)
    df = data_frame
    player_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['Name'].strip('*+').lower() in player_name.lower():
            player_df = player_df.append(row, ignore_index=True)
    return player_df




# call the functions
df = create_collection()
create_position_csv(df)
