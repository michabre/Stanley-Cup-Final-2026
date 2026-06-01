"""
Case Study: Scoring in the Stanley Cup Final
"""
import os
import pandas as pd
import numpy as np


def get_csvs(folder):
    # Filter only files
    with os.scandir(folder) as entries:
        return [entry.path for entry in entries if entry.is_file()]


# TEAM STATS
east = get_csvs('data/CAR')
west = get_csvs('data/VGK')
east_goalie = 'data/goalies/frederik_andersen.csv'
west_goalie = 'data/goalies/carter_hart.csv'


def get_player_data(player):
    # Monte-Carlo step: each call samples one of the player's real games at
    # random, so repeated simulations build a distribution of outcomes.
    player_df = pd.read_csv(player, usecols=["G", "A", "SOG", "TOI"])
    num_games = len(player_df)
    random_num = np.random.randint(0, num_games)
    single_game = player_df.iloc[random_num]
    return single_game


def get_goalie_save_percentage(goalie):
    goalie_df = pd.read_csv(goalie, usecols=["SV%"])
    num_games = len(goalie_df)
    random_num = np.random.randint(0, num_games)
    selected_game = goalie_df.iloc[random_num]
    return selected_game["SV%"]

def get_team_goals(team):
    goals = 0
    for player in team:
        data = get_player_data(player)
        goals = goals + int(data["G"])
    return goals

def get_team_shots_on_goal(team):
    shots = 0
    for player in team:
        data = get_player_data(player)
        shots = shots + int(data["SOG"])
    return shots


def get_score_based_save_percentages(east_team, west_team, east_goalie, west_goalie):
    east_sv_pct = get_goalie_save_percentage(east_goalie)
    west_sv_pct = get_goalie_save_percentage(west_goalie)
    east_sog = get_team_shots_on_goal(east_team)
    west_sog = get_team_shots_on_goal(west_team)

    east_goals = round(east_sog - (east_sog * west_sv_pct))
    west_goals = round(west_sog - (west_sog * east_sv_pct))
    return east_goals, west_goals


def predictor(count):
    index = []
    rows = []
    for i in range(count):
        index.append(f'Game {i + 1}')
        rows.append([get_team_goals(east), get_team_goals(west)])

    games_played = pd.DataFrame(rows, index=index, columns=['EAST', 'WEST'])

    west_wins = games_played.loc[games_played['WEST'] > games_played['EAST']]
    east_wins = games_played.loc[games_played['EAST'] > games_played['WEST']]
    tie_games = games_played.loc[games_played['EAST'] == games_played['WEST']]

    print(f"WEST wins: {len(west_wins)}")
    print(f"EAST wins: {len(east_wins)}")
    print(f"Tie Games {len(tie_games)}")


def predict_final_score(count):
    arr = [['', 'Final Score']]
    for i in range(count):
        arr.append(['Game ' + str(i + 1), str(get_team_goals(east)) + " - " + str(get_team_goals(west))])

    data = np.array(arr)

    games_played = pd.DataFrame(data=data[1:, 1:],
                                index=data[1:, 0],
                                columns=data[0, 1:])

    print(games_played['Final Score'].mode())
    print(games_played)


def predict_score_based_on_goalies(count):
    index = []
    rows = []
    for i in range(count):
        east_goals, west_goals = get_score_based_save_percentages(east, west, east_goalie, west_goalie)
        index.append(f'Game {i + 1}')
        rows.append([east_goals, west_goals])

    games_played = pd.DataFrame(rows, index=index, columns=['EAST', 'WEST'])

    west_wins = games_played.loc[games_played['WEST'] > games_played['EAST']]
    east_wins = games_played.loc[games_played['EAST'] > games_played['WEST']]
    tie_games = games_played.loc[games_played['EAST'] == games_played['WEST']]

    print(f"WEST wins: {len(west_wins)}")
    print(f"EAST wins: {len(east_wins)}")
    print(f"Tie Games {len(tie_games)}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Based on Player Performance')
    predictor(10)
    print('-------------------------------------------------------')
    print('Based on Goalie SV%')
    predict_score_based_on_goalies(10)


