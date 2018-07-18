# -*- encoding: utf-8 -*-
from ff_data_analysis.generator import generate_csv as gen
import datetime as dt
import pandas as pd


#TODO: rename and standardize columns


# constants
undesireable_columns = ['PPR', 'DKPt', 'FDPt', 'VBD', 'OvRank']

qb_columns = ['PosRank', 'Name', 'Team', 'Age', 'G', 'GS', 'PassCmp', 'PassAtt', 'PassYds', 'PassTD', 'FantPt', 'Year']
rb_columns = ['PosRank', 'Name', 'Team', 'Age', 'G', 'GS', 'RushAtt', 'RushYds', 'Y/A', 'RushTD', 'FantPt', 'Year']
wr_te_columns = ['PosRank', 'Name', 'Team', 'Age', 'G', 'GS', 'Tgt', 'Rec', 'RecYds', 'Y/R', 'RecTD', 'FantPt', 'Year']


def get_current_year():
    return dt.datetime.now().year


def convert_column_types(data_frame):
    for column in data_frame:
        if column not in ['Name', 'Team', 'Pos']:
            data_frame[column] = pd.to_numeric(data_frame[column])
    return data_frame


def convert_column_names(data_frame):
    data_frame = data_frame.rename({'Rk' : 'Rank'}, axis='columns')
    data_frame = data_frame.rename({'Unnamed: 1' : 'Name'}, axis='columns')
    data_frame = data_frame.rename({'Tm' : 'Team'}, axis='columns')
    data_frame = data_frame.rename({'FantPos' : 'Pos'}, axis='columns')
    data_frame = data_frame.rename({'Cmp' : 'PassCmp'}, axis='columns')
    data_frame = data_frame.rename({'Att' : 'PassAtt'}, axis='columns')
    data_frame = data_frame.rename({'Yds' : 'PassYds'}, axis='columns')
    data_frame = data_frame.rename({'TD' : 'PassTD'}, axis='columns')
    data_frame = data_frame.rename({'Int' : 'PassInt'}, axis='columns')
    data_frame = data_frame.rename({'Att.1' : 'RushAtt'}, axis='columns')
    data_frame = data_frame.rename({'Yds.1' : 'RushYds'}, axis='columns')
    data_frame = data_frame.rename({'TD.1' : 'RushTD'}, axis='columns')
    data_frame = data_frame.rename({'Yds.2' : 'RecYds'}, axis='columns')
    data_frame = data_frame.rename({'TD.2' : 'RecTD'}, axis='columns')
    return data_frame


def get_historical_rankings(year=(get_current_year() - 1)):
    if year > get_current_year():
        year = (get_current_year() - 1)
    url = 'https://www.pro-football-reference.com/years/%s/fantasy.htm#fantasy::none' % year
    data_frame = pd.read_html(url, skiprows=1, header=0)[0]
    data_frame = data_frame.drop(undesireable_columns, axis=1)
    data_frame = convert_column_names(data_frame)
    #data_frame = data_frame.rename({'Unnamed: 1' : 'Name'}, axis='columns')
    data_frame = data_frame[data_frame.Rank != 'Rk']
    data_frame = convert_column_types(data_frame)
    gen.write_historical_rankings(data_frame, year)
    return data_frame


def get_past_five_historical_rankings():
    data_frame = pd.DataFrame()
    current_year = get_current_year()
    for year in range((current_year - 5), current_year):
        year_data_frame = get_historical_rankings(year)
        year_data_frame['Year'] = year
        data_frame = data_frame.append(year_data_frame, ignore_index=True)
    gen.write_historical_rankings(data_frame)
    return data_frame


def parse_by_player_position(data_frame):
    qb_data_frame = data_frame[data_frame.Pos == 'QB']
    rb_data_frame = data_frame[data_frame.Pos == 'RB']
    wr_data_frame = data_frame[data_frame.Pos == 'WR']
    te_data_frame = data_frame[data_frame.Pos == 'TE']

    qb_data_frame = qb_data_frame[qb_columns].rename({'PosRank' : 'Rank'}, axis='columns')
    rb_data_frame = rb_data_frame[rb_columns].rename({'PosRank' : 'Rank'}, axis='columns')
    wr_data_frame = wr_data_frame[wr_te_columns].rename({'PosRank' : 'Rank'}, axis='columns')
    te_data_frame = te_data_frame[wr_te_columns].rename({'PosRank' : 'Rank'}, axis='columns')
    collection = {'QB' : qb_data_frame, 'RB' : rb_data_frame, 'WR' : wr_data_frame, 'TE' : te_data_frame}
    gen.write_historical_position_rankings(collection)
    return collection
