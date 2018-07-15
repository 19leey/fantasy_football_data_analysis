# -*- encoding: utf-8 -*-
import pandas as pd


dir_path = 'output/historical/'


def write_historical_rankings(data_frame, year=None):
    if year:
        data_frame.to_csv(('%s%s_season_rankings.csv' % (dir_path, year)), index=False)
    else:
        data_frame.to_csv(('%spast_five_season_rankings.csv' % dir_path), index=False)


def write_position_rankings(collection):
    for position in collection:
        collection[position].to_csv(('%s%s_data.csv' % (dir_path, position.lower())), index=False)
