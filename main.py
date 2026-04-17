"""
Case Study: Scoring in the Stanley Cup Final
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_csvs(folder):
    # Filter only files
    with os.scandir(folder) as entries:
        return [entry.path for entry in entries if entry.is_file()]


# TEAM STATS
home = get_csvs('data/edm')
visitor = get_csvs('data/fla')


def get_player_data(player):
    player_df = pd.read_csv(player, usecols=["G", "A", "TOI"])
    num_games = len(player_df)
    random_num = np.random.randint(0, num_games)
    single_game = player_df.iloc[random_num]
    return single_game


def get_team_goals(team):
    goals = 0
    for player in team:
        data = get_player_data(player)
        goals = goals + int(data["G"])
    return goals


def predictor(count):
    arr = [['', 'HOME', 'VISITOR']]
    for i in range(count):
        arr.append(['Game ' + str(i + 1), get_team_goals(home), get_team_goals(visitor)])

    data = np.array(arr)

    games_played = pd.DataFrame(data=data[1:, 1:],
                                index=data[1:, 0],
                                columns=data[0, 1:])

    visitor_wins = games_played.loc[games_played['VISITOR'] > games_played['HOME']]
    home_wins = games_played.loc[games_played['HOME'] > games_played['VISITOR']]
    tie_games = games_played.loc[games_played['HOME'] == games_played['VISITOR']]

    print("VISITOR wins: " + str(len(visitor_wins)))
    print("HOME wins: " + str(len(home_wins)))
    print("Tie Games " + str(len(tie_games)))


def predict_final_score(count):
    arr = [['', 'Final Score']]
    for i in range(count):
        arr.append(['Game ' + str(i + 1), str(get_team_goals(home)) + " - " + str(get_team_goals(visitor))])

    data = np.array(arr)

    games_played = pd.DataFrame(data=data[1:, 1:],
                                index=data[1:, 0],
                                columns=data[0, 1:])

    print(games_played['Final Score'].mode())
    # print(games_played)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    predictor(100)
    # predict_final_score(100)
