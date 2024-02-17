#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np


def web_scrapper(team_id1=1718, team_id2=1563):
    tournaments = []
    date = []
    home_team = []
    home_team_goals = []
    awy_team = []
    awy_team_goals = []

    url = requests.get(f'https://www.soccerbase.com/teams/head_to_head.sd?team_id={team_id1}&team2_id={team_id2}')
    soup = bs(url.text)

    for i in soup.find_all('td', class_='first tournament'):
        tournaments.append(i.text)

    for i in soup.find_all('td', class_='dateTime'):
        date.append(i.find('a', title=True).text)

    for i in soup.find_all('td', class_='team homeTeam'):
        home_team.append(i.text)

    for i in soup.find_all('a', title='View Match info'):
        home_team_goals.append(int(i.text[0]))

    for i in soup.find_all('td', class_='team awayTeam'):
        awy_team.append(i.text)

    for i in soup.find_all('a', title='View Match info'):
        awy_team_goals.append(int(i.text[-1]))

    ## Dataframe
    df_dict = {}

    df_dict['Tournaments'] = tournaments
    df_dict['Date'] = date
    df_dict['Home_Team'] = home_team
    df_dict['Home_Goals'] = home_team_goals
    df_dict['Awy_Team'] = awy_team
    df_dict['Awy_Goals'] = awy_team_goals

    df = pd.DataFrame(df_dict)

    ## Formatting Date
    new_dt = []
    for i in df['Date']:
        new_dt.append(i[3:])

    df['new_dt'] = new_dt
    df['new_dt'] = pd.to_datetime(df['new_dt'])

    df.drop('Date', axis=1, inplace=True)
    df.rename(columns={'new_dt': 'Date'}, inplace=True)
    df = df[['Tournaments', 'Date', 'Home_Team', 'Home_Goals', 'Awy_Team', 'Awy_Goals']]

    ## Winning team
    df['win_team'] = np.where((df['Home_Goals'] > df['Awy_Goals']), df['Home_Team'], df['Awy_Team'])
    df['win_team'] = np.where(df['Home_Goals'] == df['Awy_Goals'], 'Draw', df['win_team'])

    teams = df['Home_Team'].unique()
    df.to_csv(f'{teams[0]}-vs-{teams[1]}.csv')
    return df



web_scrapper()