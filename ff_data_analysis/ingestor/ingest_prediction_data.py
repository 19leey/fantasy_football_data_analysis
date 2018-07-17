# -*- encoding: utf-8 -*-
from ff_data_analysis.generator import generate_csv as gen
from pandas.compat import StringIO
from bs4 import BeautifulSoup
import urllib.request
import datetime as dt
import pandas as pd
import re


# constants
overall_columns = ['Rank', 'Overall (Team)', 'Pos', 'Best', 'Worst', 'Avg', 'Std Dev']
qb_columns = ['Rank', 'Quarterbacks (Team)', 'Best', 'Worst', 'Avg', 'Std Dev']
rb_columns = ['Rank', 'Running Backs (Team)', 'Best', 'Worst', 'Avg', 'Std Dev']
wr_columns = ['Rank', 'Wide Receivers (Team)', 'Best', 'Worst', 'Avg', 'Std Dev']
te_columns = ['Rank', 'Tight Ends (Team)', 'Best', 'Worst', 'Avg', 'Std Dev']
k_columns = ['Rank', 'Kickers (Team)', 'Best', 'Worst', 'Avg', 'Std Dev']
dst_columns = ['Rank', 'Team DST', 'Best', 'Worst', 'Avg', 'Std Dev']


def get_current_date():
    return dt.datetime.now()


def get_position_columns(position=None):
    if position:
        if position is 'qb':
            return qb_columns
        elif position is 'rb':
            return rb_columns
        elif position is 'wr':
            return wr_columns
        elif position is 'te':
            return te_columns
        elif position is 'k':
            return k_columns
        elif position is 'dst':
            return dst_columns
    else:
        return overall_columns


def drop_non_numeric(data_frame):
    indexes = []
    for index, row in data_frame.iterrows():
        if re.search('^\D', row['Rank']):
            indexes.append(index)
    data_frame = data_frame.drop(data_frame.index[indexes])
    return data_frame


def convert_column_types(data_frame, position=None):
    for column in data_frame:
        if column not in [get_position_columns(position)[1], 'Pos']:
            data_frame[column] = pd.to_numeric(data_frame[column])
    return data_frame


def rename_columns(data_frame, position=None):
    data_frame = data_frame.rename({get_position_columns(position)[1] : 'Name'}, axis='columns')
    return data_frame


def get_html_data(position=None):
    if position:
        url = 'https://www.fantasypros.com/nfl/rankings/%s-cheatsheets.php' % position
    else:
        url = 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php'
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs={'class' : 'table table-bordered table-striped player-table table-hover pad-below'})

    headers = []
    for header in table.find_all('th'):
        if 'none' not in header.get('style'):
            headers.append(header.text)
    headers.remove('WSID')

    rows = []
    for table_row in table.find_all('tr')[2:]:
        row = []
        if 'rank-table-ad' in table_row.get('class'):
            continue
        for table_cell in table_row.find_all('td'):
            if table_cell.find('input') != None:
                row.append(('%s %s' % (table_cell.find('input').get('data-name'), table_cell.find('input').get('data-team'))))
            elif table_cell.get('class'):
                if 'player-label' in table_cell.get('class'):
                    continue
                else:
                    row.append(table_cell.text)
            else:
                row.append(table_cell.text)
        rows.append(row)

    text_data = ','.join(headers)
    for row in rows:
        text_data += ('\n%s' % ','.join(row))

    data_frame = pd.read_csv(StringIO(text_data))
    return data_frame


def get_consensus_rankings(position=None):
    data_frame = get_html_data(position)
    data_frame = data_frame[get_position_columns(position)]
    data_frame = drop_non_numeric(data_frame)
    data_frame = convert_column_types(data_frame, position)
    data_frame = rename_columns(data_frame, position)
    #gen.write_raw_consensus_rankings(data_frame, position)
    return data_frame
