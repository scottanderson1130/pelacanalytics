import requests
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import pandas as pd
from sys import argv
import re

team_url = 'https://www.basketball-reference.com/teams/{team}/'
team_season_url = 'https://www.basketball-reference.com/teams/{team}/{year}.html'
go_on = False

team_stats_list = {
    1: 'all_roster',
    2: 'all_team_and_opponent',
    3: 'all_team_misc',
    4: 'all_per_game',
    5: 'all_totals',
    6: 'all_per_minute',
    7: 'all_per_poss',
    8: 'all_advanced',
    9: 'all_adj-shooting',
    10: 'all_shooting',
    11: 'all_pbp',
    12: 'all_salaries2',

}
team = input('Input team initial: ')
season = input('Season: ')
season_url = team_season_url.format(team=team, year=season)

res = requests.get(season_url)
soup = BS(res.content, 'html.parser')

while (not go_on):
    print('(1) Roster')
    print('(2) Team & Opponent Stats')
    print('(3) Team Misc.')
    print('(4) Per Game Average')
    print('(5) Totals')
    print('(6) Per 36 Min')
    print('(7) Per 100 Poss')
    print('(8) Advanced')
    print('(9) Adj. Shooting')
    print('(10) Shooting')
    print('(11) Play-by-Play')
    print('(12) Salaries')
    stat_type = int(input('Select stat by number: '))

    if (stat_type < 1 or stat_type > 12):
        print('selection must be between 1 & 12')
    else:
        go_on = True

if (stat_type != 1 and stat_type != 4 and stat_type != 8):
    placeholder = soup.select_one(
        f'#{team_stats_list[stat_type]} .placeholder')
    comment = next(
        elem for elem in placeholder.next_siblings if isinstance(elem, Comment))
    table = BS(comment, 'html.parser')
    table = table.find('table')
else:
    table = soup.find(id='all_roster')

table = str(table)

df = pd.read_html(table)[0]
df.fillna(0, inplace=True)

print(season_url)

try:
    if argv[1] == '--save':
        filename = (team).upper() + '.csv'
        df.to_csv('data/{}'.format(filename))
except IndexError:
    print(df)
