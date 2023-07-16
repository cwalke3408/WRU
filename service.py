import pandas as pd

from excel_file import *
from constants import *


def retrieve_nfl_players_by_college(college_excel_file, excel_columns):
    nfl_by_college_df = pd.read_excel(college_excel_file, usecols=excel_columns)
    return nfl_by_college_df

# Retrieve nfl players by school, draft year, and position
# https://codeshare.co.uk/blog/regular-expression-regex-for-a-number-greater-than-1200/
def filter_players_by_draft_yr_and_position(players_pf, position, draft_yr_regex):
    # Filter from draft year and by Pos
    return players_pf[(players_pf['2'].str.contains(draft_yr_regex, regex=True)) & (players_pf['Pos'] == position)]

def retrieve_players_stats(players_stat_file):
    players_stat_df = pd.read_excel(players_stat_file)
    return players_stat_df

def filter_stats_by_players_given(players_df, stats_df):    
    playerList = players_df['Player'].tolist()
    stats = stats_df[stats_df['Player'].str.contains('|'.join(playerList))]
    return stats

def is_player_excluded(player_not_to_include_list, stat_row):
    for player_dict in player_not_to_include_list:
        if((stat_row['Player'] == player_dict['player']) & (stat_row['Tm'] != player_dict['nfl_team'])):
            return True

    return False

def sum_up_total_stats_from_all_players(players_stats_df, stat_category_dict):
    for index, row in players_stats_df.iterrows():
        only_include_clem_mike_williams = dict({"player":"Mike Williams", "nfl_team": "LAC"})
        exception_list = []
        exception_list.append(only_include_clem_mike_williams.copy())

        if(is_player_excluded(exception_list, row)):
            continue

        for stat in stat_category_dict:
            stat_category_dict[stat] += row[stat]

    return stat_category_dict

def print_stats(stat_dict):
    for stat in stat_dict:
        print("Total {stat_name}: {stat_value}".format(stat_name = stat, stat_value = stat_dict[stat]))

def get_total_players_stats(players_stats_df, stat_names):
    total = players_stats_df[stat_names].sum()
    return total

def calculateThroughYears(startYr, endYr, players_df, workbook, writer):
    total_dict = dict({"Yds":0, "TD":0, "GS":0})

    # EXCEL HEADER
    worksheet = workbook.add_worksheet()
    worksheet = create_excel_header_cols(worksheet)

    row = 1
    for yr in range(startYr, endYr+1):
        yr_file = NFL_WR_STATS_FILE + str(yr) +".xlsx"
        players_stats_by_year = retrieve_players_stats(yr_file)
        filtered_stats = filter_stats_by_players_given(players_df, players_stats_by_year)

        # print("===YEAR: ", yr, "====")
        total = get_total_players_stats(filtered_stats, ['Yds','TD', 'GS'])
        # print(total)

        # print(filtered_stats[['Player','Yds','TD', 'GS']])
        total_dict['Yds'] += total['Yds']
        total_dict['TD'] += total['TD']
        total_dict['GS'] += total['GS']
        # print()

        worksheet = insert_row_data(worksheet, row, yr, total)
        row = row + 1

    # sum_col(worksheet)  # Maybe use Pandas to find sum
    workingTable(writer)
    closeExcelFile(workbook)
    return total_dict