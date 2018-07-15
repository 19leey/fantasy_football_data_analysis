# -*- encoding: utf-8 -*-
from ff_data_analysis.ingestor import ingest_data as ingest

#from ff_data_analysis.generator import render_tiers as ren
import argparse


parser = argparse.ArgumentParser()
#parser.add_argument('points', help='list of points to be mapped')
args = parser.parse_args()


#season_data = ingest.get_historical_rankings(2015)
historical_data = ingest.get_past_five_historical_rankings()
position_data = ingest.parse_by_player_position(historical_data)
print(ingest.get_consensus_rankings())
