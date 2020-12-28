import requests
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import pandas as pd
from sys import argv
import re

letter_url = 'https://www.basketball-reference.com/players/{letter}/'
players_url = 'https://www.basketball-reference.com/players/{letter}/{player_code}.html'
go_on = False

stats_list = {
    1: 'per_game',
    2: 'all_totals',
    3: 'all_per_minute',
    4: 'all_per_poss',
    5: 'all_advanced',
    6: 'all_adj-shooting',
    7: 'all_shooting',
    8: 'all_pbp'
}


def player_info(tag, url):
    for player_code in tag:
        node = str(player_code)
        player_code = "".join(re.split('href="/players/[a-z]/', node))
        player_split = " ".join(re.split('.html">', player_code))
        player_node = (re.split('<a|</a>', player_split))
        player_trim = ' '.join(player_node).strip().split(' ')

        players_code = player_trim[0]
        players_name = " ".join(player_trim[1:])

        if (players_name.lower() == inputted_player_name.lower()):
            url = players_url.format(
                letter=letter_to_request, player_code=players_code)
            print(url)
            return url


player_first_name = input("Player first name: ")
player_last_name = input("Player last name: ")

while (not go_on):
    print('(1) Per Game')
    print('(2) Totals')
    print('(3) Per 36 Minutes')
    print('(4) Per 100 Possesions')
    print('(5) Advanced')
    print('(6) Adjusted Shooting')
    print('(7) Shooting')
    print('(8) Play-By-Play')
    stat_type = int(input('Select stat by number: '))

    if (stat_type < 1 or stat_type > 8):
        print('selection must be between 1 & 8')
    else:
        go_on = True

inputted_player_name = f'{player_first_name} {player_last_name}'
letter_to_request = player_last_name[0].lower()
letter_url = letter_url.format(letter=letter_to_request)

res = requests.get(letter_url)
soup = BS(res.content, 'html.parser')
section = soup.find_all('th')
a_tags = [th.find('a', href=True) for th in section]

res = requests.get(player_info(a_tags, players_url))
soup = BS(res.content, 'html.parser')

if (stat_type > 1):
    placeholder = soup.select_one(f'#{stats_list[stat_type]} .placeholder')
    comment = next(
        elem for elem in placeholder.next_siblings if isinstance(elem, Comment))
    table = BS(comment, 'html.parser')
    table = table.find('table')
else:
    table = soup.find(id='per_game')

table = str(table)

df = pd.read_html(table)[0]
df.fillna(0, inplace=True)

try:
    if argv[1] == '--save':
        filename = (player_first_name+player_last_name).upper() + '.csv'
        df.to_csv('data/{}'.format(filename))
except IndexError:
    print(df)
