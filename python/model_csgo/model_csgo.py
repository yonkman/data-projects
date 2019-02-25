import hltvscrape
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import datetime as dt
import numpy as np

# input
teams = ['Astralis', 'Liquid', 'Natus%20Vincere', 'MIBR', 'Renegades', 'FaZe', 'ENCE', 'NiP', 
            'Cloud9', 'Vitality', 'AVANGAR', 'compLexity', 'G2', 'HellRaisers', 'BIG', 'NRG']



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# don't look like a bot
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
# on 400 error get another user-agent here: https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/

today_str = dt.datetime.today().strftime('%Y-%m-%d')
start_str = (dt.datetime.today() - dt.timedelta(weeks=52)).strftime('%Y-%m-%d')

summary_df = pd.DataFrame(columns=['team', 'team_rating', 'player', 'hltv_rating', 'kills_rating', 'avg_opponent_rating'])
allplayers_df = pd.DataFrame()

# loop through each team on the list
for i in range(len(teams)):

    # search for team on hltv
    url = "https://www.hltv.org/search?query=" + teams[i]
    print(url)
    req = Request(url=url, headers=headers) 
    html = urlopen(req).read().decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'lxml') 
    print('team ' + str(i + 1) + '/' + str(len(teams)))
  
  
    # grab the first link in the 'Teams' table
    tables = soup.find_all(class_="table") 
    for k in range(len(tables)):
        if tables[k].text.split()[0] == 'Team':
            table = tables[k]
        
    teamlink = table.find('a', href=True)
    teamlink_str = teamlink['href']
    
    # navigate to that team's profile
    url = "https://www.hltv.org" + teamlink_str        
    print(url)
    req = Request(url=url, headers=headers) 
    html = urlopen(req).read().decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'lxml')
    
    # grab the team's current roster
    players = soup.find_all(class_="text-ellipsis bold")

    team_df = pd.DataFrame()
    
    # loop through each player on the current team 
    for j in range(len(players)):
        player_str = players[j].text
        
        player_id = soup.find('a', href=True, title=player_str)
        if player_id is not None:
            id_str = player_id['href'].split('/')[2] # hltv-specific code
        
        player_df = hltvscrape.getPlayerMapHistory(player_str=player_str, player_id=id_str, start_str=start_str, end_str=today_str, deep_dive=True)
        player_df['player'] = player_str
        player_df['opponent_rating'] = np.nan
        player_df['performance_rating'] = np.nan
        player_df['kd_performance_rating'] = np.nan
        player_df['performance_weight'] = np.nan
        
        for k in range(len(player_df)):
    
            # map the hltv rank of each opponent to a rating:
        
            # 1 -> 2000
            # 10 -> 1687
            # 20 -> 1405
            # 30 -> 1194
            # unranked -> 800
        
            # R = 0.348118625*x^2 - 38.597933448*x+2038.249936559
            
            if player_df.loc[k, 'opponent_rank'] is np.nan: # (np.nan == np.nan) -> False, (np.nan is np.nan) -> True
                player_df.loc[k, 'opponent_rating'] = 800
                
            else:
                x = float(player_df.loc[k, 'opponent_rank'])
                player_df.loc[k, 'opponent_rating'] = 0.348118625*x**2 - 38.597933448*x + 2038.249936559
    
            player_df.loc[k, 'performance_rating'] = player_df['opponent_rating'].loc[k]*float(player_df['hltv_rating'].loc[k])
            player_df.loc[k, 'kd_performance_rating'] = player_df['opponent_rating'].loc[k]*float(player_df['kills'].loc[k])/float(player_df['deaths'].loc[k])
            
        print(teams[i] + '\t' + player_str + '\t')
        print(str(len(player_df)) + ' games found.')
        print('Mean opponent rating: ' + str(float(player_df['opponent_rating'].mean())))
        print('hltv rating: ' + str(float(player_df['performance_rating'].mean())) + '\tkills rating: ' + str(float(player_df['kd_performance_rating'].mean())))
        print()
        summary_df.loc[5*i + j, 'team'] = teams[i]
        summary_df.loc[5*i + j, 'player',] = player_str
        summary_df.loc[5*i + j, 'hltv_rating'] = float(player_df['kd_performance_rating'].mean())
        summary_df.loc[5*i + j, 'kills_rating'] = float(player_df['performance_rating'].mean())
        summary_df.loc[5*i + j, 'avg_opponent_rating'] = float(player_df['opponent_rating'].mean())
        
        team_df = team_df.append(player_df)
        allplayers_df = pd.concat([allplayers_df, player_df])
        # player_df.to_csv(player_str + '_' + today_str + '.csv', encoding='utf-8', index=False)
        # to print a file for each player

        # 
        # calculate, for each map:
        #   opponent_rating: fit to map curve
        #   performance_rating: hltv_rating*opponent_rating
        #   performance_weight: should be high when performing well against a better team or poorly against a worse team
        #                       low in the opposite case
        #                       zero if the player did well but against a much worse team (if a team wins convincingly their rating should never go down)
        #   it may be useful to first determine the average opponent rating of the team
        
        #   ex: 
        #   opponent_rating = 2000; hltv_rating = 1.4; I want performance_weight to be about 2.0
        #   opponent_rating = 1194; hltv_rating = 0.6; I want performance_weight to be about 2.0
        #   opponent_rating = anything; hltv_rating = 1.0; I want performance_weight to be about 1.0
        #   opponent_rating = 2000; hltv_rating = 0.6; I want performance_weight to be about 0.75
        #   opponent_rating = 1194; hltv_rating = 1.4; I want performance_weight to be about 0.5
        
        #   if opponent_rating = 800 (unranked), apply a 0.5x multiplier to performance_weight
        
        # plot performance_rating on a scatter plot with marker size or colour showing performance_weight
        
    # team_df.to_csv(teams[i] + '_' + today_str + '.csv', encoding='utf-8', index=False)
    # to print a file for each team
    print()
    print()

print(summary_df.head(50))    

summary_df.to_csv('summary.csv')
allplayers_df.to_csv('IEM_Katowice_players.csv')
