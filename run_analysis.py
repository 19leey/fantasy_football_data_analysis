# -*- encoding: utf-8 -*-
from ff_data_analysis.ingestor import ingest_historical_data as hd
from ff_data_analysis.ingestor import ingest_prediction_data as pd
from ff_data_analysis.cluster import cluster_data as cd
from ff_data_analysis.generator import render_tiers as ren
import argparse


parser = argparse.ArgumentParser()
#parser.add_argument()
args = parser.parse_args()


# historical data
season_data = hd.get_historical_rankings(2015)
historical_data = hd.get_past_five_historical_rankings()
position_data = hd.parse_by_player_position(historical_data)


# consensus data
overall_consensus_data = pd.get_consensus_rankings()
cd.cluster_overall_rankings(overall_consensus_data)
position_consensus_data = {}
positions = ['qb', 'rb', 'wr', 'te', 'k', 'dst']
for position in positions:
    position_consensus_data[position] = pd.get_consensus_rankings(position)
    cd.cluster_position_rankings(position_consensus_data[position], position)


# plot data
ren.run_rscript()
