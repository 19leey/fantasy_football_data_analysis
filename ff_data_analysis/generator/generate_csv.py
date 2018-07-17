# -*- encoding: utf-8 -*-
import pandas as pd


# constants
historical_dir_path = 'output/historical/'
raw_consensus_dir_path = 'output/consensus/raw/'
clustered_consensus_dir_path = 'output/consensus/clustered/'


def write_historical_rankings(data_frame, year=None):
    if year:
        data_frame.to_csv(('%s%s_season_rankings.csv' % (historical_dir_path, year)), index=False)
    else:
        data_frame.to_csv(('%spast_five_season_rankings.csv' % historical_dir_path), index=False)


def write_historical_position_rankings(collection):
    for position in collection:
        collection[position].to_csv(('%s%s_data.csv' % (historical_dir_path, position.lower())), index=False)


def write_raw_consensus_rankings(data_frame, position=None):
    if position:
        data_frame.to_csv(('%s%s_rankings.csv' % (raw_consensus_dir_path, position)), index=False)
    else:
        data_frame.to_csv(('%soverall_rankings.csv' % raw_consensus_dir_path), index=False)


def write_clustered_consensus_rankings(data_frame, position=None):
    if position:
        data_frame.to_csv(('%sclustered_%s_rankings.csv' % (clustered_consensus_dir_path, position)), index=False)
    else:
        for slice in data_frame:
            data_frame[slice].to_csv(('%sclustered_overall_rankings_%s.csv' % (clustered_consensus_dir_path, slice)), index=False)
