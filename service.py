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



#       Rk              Player   Tm  Age Pos   G  GS  Tgt  Rec  Ctch%   Yds   Y/R  TD  1D  Lng  Y/Tgt  R/G    Y/G  Fmb
# 0      1  Justin Jefferson*+  MIN   23  WR  17  17  184  128  0.696  1809  14.1   8  80   64    9.8  7.5  106.4    0
# 1      2       Tyreek Hill*+  MIA   28  WR  17  17  170  119  0.700  1710  14.4   7  77   64   10.1  7.0  100.6    1
# 2      3      Travis Kelce*+  KAN   33  TE  17  17  152  110  0.724  1338  12.2  12  78   52    8.8  6.5   78.7    1
# 3      4       Stefon Diggs*  BUF   29  WR  16  16  154  108  0.701  1429  13.2  11  74   53    9.3  6.8   89.3    1
# 4      5       Austin Ekeler  LAC   27  RB  17  17  127  107  0.843   722   6.7   5  36   23    5.7  6.3   42.5    5
# ..   ...                 ...  ...  ...  ..  ..  ..  ...  ...    ...   ...   ...  ..  ..  ...    ...  ...    ...  ...
# 503  504         Noah Togiai  PHI   25  TE   2   0    1    0  0.000     0   NaN   0   0    0    0.0  0.0    0.0    0
# 504  505         Jake Tonges  CHI   23  TE   4   0    1    0  0.000     0   NaN   0   0    0    0.0  0.0    0.0    0
# 505  506           DJ Turner  LVR   25  WR   9   0    1    0  0.000     0   NaN   0   0    0    0.0  0.0    0.0    1
# 506  507    James Washington  DAL   26  WR   2   0    1    0  0.000     0   NaN   0   0    0    0.0  0.0    0.0    0
def retrieve_players_stats(players_stat_file):
    players_stat_df = pd.read_excel(players_stat_file)
    return players_stat_df



#       Rk            Player   Tm  Age Pos   G  GS  Tgt  Rec  Ctch%   Yds   Y/R  TD  1D  Lng  Y/Tgt  R/G   Y/G  Fmb
# 19    20    Garrett Wilson  NYJ   22  WR  17  12  147   83  0.565  1103  13.3   4  56   60    7.5  4.9  64.9    2
# 25    26   Terry McLaurin*  WAS   27  WR  17  17  120   77  0.642  1191  15.5   5  56   52    9.9  4.5  70.1    1
# 34    35       Chris Olave  NOR   22  WR  15   9  119   72  0.605  1042  14.5   4  48   53    8.8  4.8  69.5    2
# 43    44     Curtis Samuel  WAS   26  WR  17  12   92   64  0.696   656  10.3   4  36   49    7.1  3.8  38.6    1
# 45    46   Parris Campbell  IND   25  WR  17  16   91   63  0.692   623   9.9   3  32   49    6.8  3.7  36.6    1
# 91    92        Noah Brown  DAL   26  WR  16  13   74   43  0.581   555  12.9   3  25   51    7.5  2.7  34.7    1
# 229  230    Michael Thomas  NOR   29  WR   3   3   22   16  0.727   171  10.7   3  13   21    7.8  5.3  57.0    0
# 482  483  Jameson Williams  DET   21  WR   6   0    9    1  0.111    41  41.0   1   1   41    4.6  0.2   6.8    0
def filter_stats_by_players_given(players_df, stats_df):    
    playerList = players_df['Player'].tolist()
    stats = stats_df[stats_df['Player'].str.contains('|'.join(playerList))]
    return stats

def is_player_excluded(player_not_to_include_list, stat_row):
    for player_dict in player_not_to_include_list:
        if((stat_row['Player'] == player_dict['player']) & (stat_row['Tm'] != player_dict['nfl_team'])):
            return True

    return False

# def sum_up_total_stats_from_all_players(players_stats_df, stat_category_dict):
#     for index, row in players_stats_df.iterrows():
#         only_include_clem_mike_williams = dict({"player":"Mike Williams", "nfl_team": "LAC"})
#         exception_list = []
#         exception_list.append(only_include_clem_mike_williams.copy())

#         if(is_player_excluded(exception_list, row)):
#             continue

#         for stat in stat_category_dict:
#             stat_category_dict[stat] += row[stat]

#     return stat_category_dict

def print_stats(stat_dict):
    for stat in stat_dict:
        print("Total {stat_name}: {stat_value}".format(stat_name = stat, stat_value = stat_dict[stat]))

def get_total_players_stats(players_stats_df, stat_names):
    total = players_stats_df[stat_names].sum()
    return total

# def calculateThroughYears(startYr, endYr, players_df, workbook, writer):
#     total_dict = dict({"Yds":0, "TD":0, "GS":0})

#     # EXCEL HEADER
#     worksheet = workbook.add_worksheet()
#     worksheet = create_excel_header_cols(worksheet)

#     row = 1
#     for yr in range(startYr, endYr+1):
#         yr_file = NFL_WR_STATS_FILE + str(yr) +".xlsx"
#         players_stats_by_year = retrieve_players_stats(yr_file)
#         filtered_stats = filter_stats_by_players_given(players_df, players_stats_by_year)

#         # print("===YEAR: ", yr, "====")
#         total = get_total_players_stats(filtered_stats, ['Yds','TD', 'GS'])
#         # print(total)

#         # print(filtered_stats[['Player','Yds','TD', 'GS']])
#         total_dict['Yds'] += total['Yds']
#         total_dict['TD'] += total['TD']
#         total_dict['GS'] += total['GS']
#         # print()

#         worksheet = insert_row_data(worksheet, row, yr, total)
#         row = row + 1

#     # sum_col(worksheet)  # Maybe use Pandas to find sum
#     workingTable(writer)
#     closeExcelFile(workbook)
#     return total_dict


# Fill stats by year and college
# 
# | YEAR | Yards | TDs | GS |
# | 2012 |   x   |  y  | z  |
# | 2013 |   x   |  y  | z  |
#   ...
# | 2022 |   x   |  y  | z  |
def getStatsByYears(startYr, endYr, players_df, writer, teamName):
    statsByYear = []
    yardsByYear = []
    touchdownByYear = []
    gameStartByYear = []
    startRow = endYr - startYr + 7
    
    for yr in range(startYr, endYr+1):
        yr_file = NFL_WR_STATS_FILE + str(yr) +".xlsx"
        players_stats_by_year = retrieve_players_stats(yr_file)
        filtered_stats_df = filter_stats_by_players_given(players_df, players_stats_by_year)

        #Enter player stat details to result file
        year_df = pd.DataFrame({ 'YEAR': [], str(yr): []})
        year_df.to_excel(writer, sheet_name=teamName, startrow=startRow-1, startcol=0, header=True)
        filtered_stats_df.to_excel(writer, sheet_name=teamName, startrow=startRow, startcol=0, header=True)
        startRow = startRow + len(filtered_stats_df.index) + 4

        total = get_total_players_stats(filtered_stats_df, ['Yds','TD', 'GS'])
        statsByYear.append(yr)
        yardsByYear.append(total['Yds'])
        touchdownByYear.append(total['TD'])
        gameStartByYear.append(total['GS'])

    df = pd.DataFrame({
        'YEAR': statsByYear,
        'Yards': yardsByYear,
        'TDs': touchdownByYear,
        'GS': gameStartByYear
    })

    return df