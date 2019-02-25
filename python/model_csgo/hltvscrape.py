# returns a df of the player's map history and their performance, optionally stores the data as csv
def getPlayerMapHistory(player_str, player_id, start_str, end_str, deep_dive):
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup
    from time import sleep
    import pandas as pd
    import datetime as dt
    import numpy as np
    
    
    
    teams_df = pd.read_csv('top30.csv')
    last_week = dt.date.fromisoformat(teams_df.loc[0, 'date'])
    print(teams_df.loc[0, 'date'])
    
    if last_week + dt.timedelta(weeks=1) < dt.date.today():
        print('New ranks available, updating top30.csv')
        # updateTop30('top30.csv')
        # updates the file each week
        
        teams_df = pd.read_csv('top30.csv')
    
    earliest_date = dt.date.fromisoformat(start_str)
    
    teams_df['parsed_time'] = pd.to_datetime(teams_df['date'], infer_datetime_format=True)
    output_df = pd.DataFrame(columns=["date","team","team_score","opponent","opponent_score","map","kills","deaths", "hltv_rating", "parsed_time", "opponent_rank"])	

    url = "https://www.hltv.org/stats/players/matches/" + player_id + "/startDate=" + start_str + "&endDate=" + end_str + "&matchType=Lan"
    print(url)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    req = Request(url=url, headers=headers) 
        
    html = urlopen(req).read() # .decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'lxml') 

    date_all = soup.find_all(class_="time")
    map_count = len(date_all)

    map_all = soup.tbody.find_all(class_="statsMapPlayed")
    kills_all = soup.tbody.find_all(class_="statsCenterText")
    deaths_all = soup.tbody.find_all(class_="statsCenterText")
    hltvrating_all = soup.find_all('td', {'class': ['match-won ratingNegative', 'match-won ratingPositive','match-lost ratingNegative', 'match-lost ratingPositive', 'match-tied ratingNegative', 'match-tied ratingPositive']})

    table = soup.find('table', {'class': 'stats-table no-sort'})
    teams_and_scores = table.find_all('span')
    
    for i in range(len(hltvrating_all)):
        
        dd, mm, yy = date_all[i].text.strip().split('/')
        if len(mm) == 1:
            mm = '0' + mm
        if len(dd) == 1:
            dd = '0' + dd
        
        date_str = "20" + yy + "-" + mm + "-" + dd
        
        if dt.date.fromisoformat(date_str) < earliest_date:
            break
        
        output_df.loc[i] = np.nan # append a new row of nans
        
        
        output_df['date'][i] = date_str
        
        output_df['map'][i] = map_all[i].text.strip()
        
        output_df['team'][i] = teams_and_scores[i*4 + 1].text.strip()
        output_df['team_score'][i] = teams_and_scores[i*4 + 2].text.strip()[1:-1]
        
        output_df['opponent'][i] = teams_and_scores[i*4 + 3].text.strip()
        output_df['opponent_score'][i] = teams_and_scores[i*4 + 4].text.strip()[1:-1]
        
        output_df['kills'][i] = kills_all[i].text.strip()[:2].strip()
        output_df['deaths'][i] = deaths_all[i].text.strip()[-2:].strip()
        
        output_df['hltv_rating'][i] = hltvrating_all[i].text.strip()
        
        output_df['parsed_time'][i] = pd.to_datetime(output_df['date'][i], infer_datetime_format=True)
        
        right_team_right_time = (teams_df['team'] == output_df['opponent'][i]) & (teams_df['parsed_time'] >= output_df['parsed_time'][i]) & (teams_df['parsed_time'] < output_df['parsed_time'][i] + dt.timedelta(weeks=1))

        selected_rows = teams_df[right_team_right_time]
        
        rating_row = selected_rows.sort_values(by='parsed_time', ascending=True)[:1]
        
        if len(rating_row['rank']) > 0:
            output_df['opponent_rank'][i] = rating_row['rank'].iloc[0]
            

    
    return output_df

    
def updateTop30(filename):
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup
    from time import sleep
    import pandas as pd
    import datetime as dt

    output_df = pd.DataFrame(columns=["date","rank","team","score"])	
    today = dt.date.fromisoformat( dt.datetime.today().strftime('%Y-%m-%d') )

    x = dt.date.fromisoformat('2019-01-21')

    while x < today:
        last = x
        x = x + dt.timedelta(weeks=1)
        

    since = dt.date.fromisoformat('2016-03-20')

    # today_str = dt.datetime.today().strftime('%Y-%m-%d')
    print(last.strftime('%Y/%B/%d').lower())
    print()
    print(since.strftime('%Y/%B/%d').lower())

        
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    i = -1

    date_inc = last
    while(date_inc >= since):
        i += 1
        if date_inc.strftime('%Y-%m-%d') == "2018-01-22":
            date_inc = date_inc + dt.timedelta(days=1)
        elif date_inc.strftime('%Y-%m-%d') == "2018-01-09":
            date_inc = date_inc - dt.timedelta(days=1)
        
        elif date_inc.strftime('%Y-%m-%d') == "2016-10-31":
            date_inc = date_inc + dt.timedelta(days=1)
        elif date_inc.strftime('%Y-%m-%d') == "2016-10-25":
            date_inc = date_inc - dt.timedelta(days=1)
            
        elif date_inc.strftime('%Y-%m-%d') == "2016-07-25":
            date_inc = date_inc + dt.timedelta(days=1)
        elif date_inc.strftime('%Y-%m-%d') == "2016-07-12":
            date_inc = date_inc - dt.timedelta(days=1)   
            
        elif date_inc.strftime('%Y-%m-%d') == "2016-06-20":
            date_inc = date_inc + dt.timedelta(days=1)
        elif date_inc.strftime('%Y-%m-%d') == "2016-06-14":
            date_inc = date_inc - dt.timedelta(days=1)
            
        elif date_inc.strftime('%Y-%m-%d') == "2016-05-30":
            date_inc = date_inc - dt.timedelta(days=7)
            
        elif date_inc.strftime('%Y-%m-%d') == "2016-05-16":
            date_inc = date_inc + dt.timedelta(days=1)      
        elif date_inc.strftime('%Y-%m-%d') == "2016-05-10":
            date_inc = date_inc - dt.timedelta(days=1)           
            
        elif date_inc.strftime('%Y-%m-%d') == "2016-04-04":
            date_inc = date_inc + dt.timedelta(days=1)      
        elif date_inc.strftime('%Y-%m-%d') == "2016-03-29":
            date_inc = date_inc - dt.timedelta(days=1)  
            
        elif date_inc.strftime('%Y-%m-%d') == "2016-02-29": # 2016 is a leap year
            date_inc = date_inc + dt.timedelta(days=1)      
        elif date_inc.strftime('%Y-%m-%d') == "2016-02-23":
            date_inc = date_inc - dt.timedelta(days=1)          
        
        elif date_inc.strftime('%Y-%m-%d') == "2016-02-08": # 2016 is a leap year
            date_inc = date_inc + dt.timedelta(days=1)      

        url = "https://www.hltv.org/ranking/teams/" + date_inc.strftime('%Y/%B/%d').lower()
        print(url)
        
        req = Request(url=url, headers=headers) 
        
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml') 


        team_all = soup.find_all('span', {'class': 'name'})
        score_all = soup.find_all('span', {'class': 'points'})
        
        for j in range(30):
            
            output_df.loc[i*30 + j] = ""
            
            output_df['date'][i*30 + j] = date_inc.strftime('%Y-%m-%d')
            
            output_df['rank'][i*30 + j] = j + 1
            
            output_df['team'][i*30 + j] = team_all[j].text.strip()
            
            output_df['score'][i*30 + j] = score_all[j].text.strip()[1:-8]
        
        print(date_inc.strftime('%Y-%m-%d'))
        
        date_inc = date_inc - dt.timedelta(weeks=1)

    output_df.to_csv(filename, encoding='utf-8', index=False)
        

    
