# pip install pandas
# pip install xlrd

import numpy as np
import pandas as pd
import csv
import xlsxwriter as excel

from excel_file import *
from constants import *
from service import *

# Link to NFL WR stats: https://www.pro-football-reference.com/years/2010/receiving.htm

# HOW TO RUN
# POWERSHELL ->
#   cd C:\Users\Chris\Documents\Code\Projects\WRU
#   python calculate_wr_stats_by_school.py

if __name__ == "__main__":
    players_df = retrieve_nfl_players_by_college(LSU_PLAYERS, [0,1,9,10,11])
    filtered_players_df = filter_players_by_draft_yr_and_position(players_df, 'WR', '^[2-9][0-9][0-9][0-9]')
    workbook = createExcelFile('LSU_WR_2012-2022')
    writer = createExcelWriter('LSU_WR_2012-2022_TEST')

    total_dict = calculateThroughYears(2012,2022,filtered_players_df,workbook, writer)
    print_stats(total_dict)
    print(filtered_players_df.to_string())





# Sort values: df.sort_values('column_name', ascending=False)
# Rename columns: 
    # Individual: df.rename(columns = {'2':'draftYr'}, implace=True)
    # All Columns: df.columns = ['Pos', 'Player', ....]
