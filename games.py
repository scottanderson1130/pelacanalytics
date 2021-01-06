import requests
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import pandas as pd
from sys import argv
import re

season_game_log = 'https://www.basketball-reference.com/teams/{team}/{year}/gamelog/'
game_log_box = 'https://www.basketball-reference.com/boxscors/{date}.html'
game_log_shot_chart = 'https://www.basketball-reference.com/boxscors/shot-chart/{date}.html'

team = input('Team initial: ')
season = input('Season: ')
season_log = season_game_log.format(team=team, year=season)

print(season_log)

res = requests.get(season_log)
soup = BS(res.content, 'html.parser')
table = soup.find(id='all_tgl_basic')
table = str(table)

df = pd.read_html(table)

print(df)
