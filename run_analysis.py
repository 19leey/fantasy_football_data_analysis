# -*- encoding: utf-8 -*-
from ff_data_analysis.ingestor import ingest_historical_data as h
from ff_data_analysis.ingestor import ingest_prediction_data as p
import argparse


parser = argparse.ArgumentParser()
#parser.add_argument('points', help='list of points to be mapped')
args = parser.parse_args()


#season_data = h.get_historical_rankings(2015)
#historical_data = h.get_past_five_historical_rankings()
#position_data = h.parse_by_player_position(historical_data)
df = p.get_consensus_rankings()
