# -*- encoding: utf-8 -*-
from ff_data_analysis.generator import generate_csv as gen
import datetime as dt
import pandas as pd


#TODO: rename and standardize columns
#TODO: fix dtypes - unecessary floats

# constants
undesireable_columns = ['PPR', 'DKPt', 'FDPt', 'VBD', 'OvRank']

qb_columns = ['PosRank', 'Name', 'Tm', 'Age', 'G', 'GS', 'Cmp', 'Att', 'Yds', 'TD', 'FantPt', 'Year']
rb_columns = ['PosRank', 'Name', 'Tm', 'Age', 'G', 'GS', 'Att.1', 'Yds.1', 'Y/A', 'TD.1', 'FantPt', 'Year']
wr_te_columns = ['PosRank', 'Name', 'Tm', 'Age', 'G', 'GS', 'Tgt', 'Rec', 'Yds.2', 'Y/R', 'TD.2', 'FantPt', 'Year']


def get_current_year():
    return dt.datetime.now().year


def dtype_to_numeric(data_frame):
    for column in data_frame:
        if column not in ['Name', 'Tm', 'FantPos']:
            data_frame[column] = pd.to_numeric(data_frame[column])
    return data_frame


def get_historical_rankings(year=(get_current_year() - 1)):
    if year > get_current_year():
        year = (get_current_year() - 1)
    url = 'https://www.pro-football-reference.com/years/%s/fantasy.htm#fantasy::none' % year
    data_frame = pd.read_html(url, skiprows=1, header=0)[0]
    data_frame = data_frame.drop(undesireable_columns, axis=1)
    data_frame = data_frame.rename({'Unnamed: 1' : 'Name'}, axis='columns')
    data_frame = data_frame[data_frame.Rk != 'Rk']
    data_frame = dtype_to_numeric(data_frame)
    #gen.write_historical_rankings(data_frame, year)
    return data_frame


def get_past_five_historical_rankings():
    data_frame = pd.DataFrame()
    current_year = get_current_year()
    for year in range((current_year - 5), current_year):
        year_data_frame = get_historical_rankings(year)
        year_data_frame['Year'] = year
        data_frame = data_frame.append(year_data_frame, ignore_index=True)
    #gen.write_historical_rankings(data_frame)
    return data_frame


def parse_by_player_position(data_frame):
    qb_data_frame = data_frame[data_frame.FantPos == 'QB']
    rb_data_frame = data_frame[data_frame.FantPos == 'RB']
    wr_data_frame = data_frame[data_frame.FantPos == 'WR']
    te_data_frame = data_frame[data_frame.FantPos == 'TE']

    qb_data_frame = qb_data_frame[qb_columns].rename({'PosRank' : 'Rk'}, axis='columns')
    rb_data_frame = rb_data_frame[rb_columns].rename({'PosRank' : 'Rk'}, axis='columns')
    wr_data_frame = wr_data_frame[wr_te_columns].rename({'PosRank' : 'Rk'}, axis='columns')
    te_data_frame = te_data_frame[wr_te_columns].rename({'PosRank' : 'Rk'}, axis='columns')
    collection = {'QB' : qb_data_frame, 'RB' : rb_data_frame, 'WR' : wr_data_frame, 'TE' : te_data_frame}
    #gen.write_position_rankings(collection)
    return collection
