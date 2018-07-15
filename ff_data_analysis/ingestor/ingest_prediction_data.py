# -*- encoding: utf-8 -*-
from ff_data_analysis.generator import generate_csv as gen
import datetime as dt
import pandas as pd


# constants
desireable_columns = ['Rank', 'Overall (Team)', 'Pos', 'Best', 'Worst', 'Avg']


def get_current_date():
    return dt.datetime.now()


def dtype_to_numeric(data_frame):
    for column in data_frame:
        if column not in ['Overall (Team)', 'Pos']:
            data_frame[column] = pd.to_numeric(data_frame[column], errors='ignore')
    return data_frame


def parse_by_tiers(data_frame):
    return None


def get_consensus_rankings():
    url = 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php?export=xls'
    data_frame = pd.read_html(url, header=0)[0]
    data_frame = data_frame[desireable_columns]
    return data_frame
