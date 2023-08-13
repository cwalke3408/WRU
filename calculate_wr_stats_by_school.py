# pip install pandas
# pip install xlrd

import numpy as np
import pandas as pd
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
    # START_YEAR = 2012
    START_YEAR = 2019
    END_YEAR = 2022
    POSITION = 'WR'
    RESULT_FILE_NAME = 'WRU_2012-2022_TEST'
    TEAMS = [
        {'teamName': 'LSU', 'teamFile': LSU_PLAYERS}, 
        {'teamName': 'BAMA', 'teamFile': BAMA_PLAYERS}, 
        {'teamName': 'CLEM', 'teamFile': CLEM_PLAYERS}, 
        {'teamName': 'OSU', 'teamFile': OHIO_ST_PLAYERS}
    ]
    writer = createExcelWriter(RESULT_FILE_NAME)


    for team in TEAMS:
        print("Collecting stats for team=" +team['teamName']+ " position=" +POSITION+ " from startYear=" +str(START_YEAR)+ " and endYear=" +str(END_YEAR))
        players_df = retrieve_nfl_players_by_college(team['teamFile'], [0,1,9,10,11])
        filtered_players_df = filter_players_by_draft_yr_and_position(players_df, POSITION, '^[2-9][0-9][0-9][0-9]')
        statsDf = getStatsByYears(START_YEAR, END_YEAR, filtered_players_df, writer, team['teamName'])
        statsDf.to_excel(writer, sheet_name=team['teamName'], startrow=2, startcol=0, header=True)

    print('Saving final results to file: ' + RESULT_FILE_NAME)
    writer.save()