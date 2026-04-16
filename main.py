"""
Case Study: Scoring in the Stanley Cup Final
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

edmonton = {
    "a_henrique": "data/edm/a_henrique.csv",
    "b_kulak": "data/edm/b_kulak.csv",
    "c_brown": "data/edm/c_brown.csv",
    "c_ceci": "data/edm/c_ceci.csv",
    "c_macdavid": "data/edm/c_macdavid.csv",
    "d_holloway": "data/edm/d_holloway.csv",
    "e_bouchard": "data/edm/e_bouchard.csv",
    "e_kane": "data/edm/e_kane.csv",
    "l_draisaitl": "data/edm/l_draisaitl.csv",
    "m_ekholm": "data/edm/m_ekholm.csv",
    "m_janmark": "data/edm/m_janmark.csv",
    "r_nugenthopkins": "data/edm/r_nugenthopkins.csv",
    "z_hyman": "data/edm/z_hyman.csv"
}

florida = {
    "a_barkov": "data/fla/a_barkov.csv",
    "a_ekblad": "data/fla/a_ekblad.csv",
    "a_lundell": "data/fla/a_lundell.csv",
    "b_montour": "data/fla/b_montour.csv",
    "c_verhaeghe": "data/fla/c_verhaeghe.csv",
    "e_luostarinen": "data/fla/e_luostarinen.csv",
    "e_rodrigues": "data/fla/e_rodrigues.csv",
    "g_forsling": "data/fla/g_forsling.csv",
    "m_tkachuk": "data/fla/m_tkachuk.csv",
    "o_ekmanlarsson": "data/fla/o_ekmanlarsson.csv",
    "s_bennett": "data/fla/s_bennett.csv",
    "s_reinhart": "data/fla/s_reinhart.csv",
    "v_tarasenko": "data/fla/v_tarasenko.csv"
}


def get_player_data(player):
    player_df = pd.read_csv(player, usecols=["G", "A", "TOI"])
    num_games = len(player_df)
    random_num = np.random.randint(0, num_games)
    single_game = player_df.iloc[random_num]
    return single_game


def get_team_goals(team):
    goals = 0
    for player in team:
        data = get_player_data(team[player])
        goals = goals + int(data["G"])
    return goals


def predictor(count):
    arr = [['', 'EDM', 'FLA']]
    for i in range(count):
        arr.append(['Game ' + str(i + 1), get_team_goals(edmonton), get_team_goals(florida)])

    data = np.array(arr)

    games_played = pd.DataFrame(data=data[1:, 1:],
                                index=data[1:, 0],
                                columns=data[0, 1:])

    florida_wins = games_played.loc[games_played['FLA'] > games_played['EDM']]
    edmonton_wins = games_played.loc[games_played['EDM'] > games_played['FLA']]
    tie_games = games_played.loc[games_played['EDM'] == games_played['FLA']]

    print("FLA wins: " + str(len(florida_wins)))
    print("EDM wins: " + str(len(edmonton_wins)))
    print("Tie Games " + str(len(tie_games)))


def predict_final_score(count):
    arr = [['', 'Final Score']]
    for i in range(count):
        arr.append(['Game ' + str(i + 1), str(get_team_goals(edmonton)) + " - " + str(get_team_goals(florida))])

    data = np.array(arr)

    games_played = pd.DataFrame(data=data[1:, 1:],
                                index=data[1:, 0],
                                columns=data[0, 1:])

    print(games_played['Final Score'].mode())
    # print(games_played)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    predictor(1000)
    # predict_final_score(100)
