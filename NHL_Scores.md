
# Visualizing final scores in the NHL: 1917 to today

I start, as I usually do - aimlessly gathering all the data I can possibly get my hands on.

## Use NHL.com API calls to gather data

My approach to data gathering goes something like this:
1. Muck around on [nhl.com/stats](http://www.nhl.com/stats/) until I find some interest
2. Use 'Inspect' (Crtl+Shit+I on Chrome/Windows) to view calls to the NHL REST API ([Check this out](http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/) for more on this)
3. Fiddle with the URL of the call till I get what I want

In this case, I wanted the results of all the games ever played in the NHL and the API seemed to truncate the data at 50k rows, so I ended up splitting the calls to the API into 5 year chunks (could have been larger sections).


```python
import json
import requests
import pandas as pd
import numpy as np
import datetime

# Get current year
now = datetime.datetime.now().year

# Create range of years to get data, starting with 1917, leading to now.
# The REST api call doesn't seem to return more that 50k lines at a time.
# So, I've split up the year range into 5 year sections (could be 10)
years = np.arange(1917,now,5)

# Ensure the final year in the range is the current year
if years[-1] != now: years[-1] = now 

# Create empty data frame
df = pd.DataFrame()
    
# For each year span, generate URL and get data
for i in range(len(years)-1):
    
    # Create URL
    URL = ("http://www.nhl.com/stats/rest"
           "/team?"
           "isAggregate=false"
           "&reportType=basic"
           "&isGame=true"
           "&reportName=teamsummary"
           "&cayenneExp=gameDate%3E=%22"
           +str(years[i])+
           "-08-01%22%20and%20gameDate%3C=%22"
           +str(years[i+1])+
           "-08-01%22%20and%20gameTypeId=2")
    
    # Get data as JSON dict from URL
    rawDict = requests.get(URL).json()
    # Convert raw data dictionary to pandas data frame
    df = df.append(pd.DataFrame.from_dict(rawDict['data']))

# Write complete data frame to CSV (not required, just for posterity)
df.to_csv('NHL_Game_Summaries_1917_'+str(int(now))+'.csv')

# Print columns of data frame for future reference
print(df.columns)

df.head

```

    Index(['faceoffWinPctg', 'faceoffsLost', 'faceoffsWon', 'gameDate', 'gameId',
           'gameLocationCode', 'gamesPlayed', 'goalsAgainst', 'goalsFor', 'losses',
           'opponentTeamAbbrev', 'otLosses', 'penaltyKillPctg', 'points',
           'ppGoalsAgainst', 'ppGoalsFor', 'ppOpportunities', 'ppPctg',
           'shNumTimes', 'shootoutGamesLost', 'shootoutGamesWon', 'shotsAgainst',
           'shotsFor', 'teamAbbrev', 'teamFullName', 'teamId', 'ties', 'wins'],
          dtype='object')
    




    <bound method NDFrame.head of       faceoffWinPctg faceoffsLost faceoffsWon              gameDate  \
    0                  0            0           0  1917-12-20T01:00:00Z   
    1                  0            0           0  1919-02-19T01:00:00Z   
    2                  0            0           0  1920-03-09T01:00:00Z   
    3                  0            0           0  1920-03-07T01:00:00Z   
    4                  0            0           0  1921-01-30T01:00:00Z   
    5                  0            0           0  1921-01-27T01:00:00Z   
    6                  0            0           0  1921-02-03T01:00:00Z   
    7                  0            0           0  1922-01-05T01:00:00Z   
    8                  0            0           0  1918-01-10T01:00:00Z   
    9                  0            0           0  1920-01-25T01:00:00Z   
    10                 0            0           0  1920-12-26T01:00:00Z   
    11                 0            0           0  1921-01-27T01:00:00Z   
    12                 0            0           0  1918-12-22T01:00:00Z   
    13                 0            0           0  1921-02-13T01:00:00Z   
    14                 0            0           0  1921-01-07T01:00:00Z   
    15                 0            0           0  1920-01-22T01:00:00Z   
    16                 0            0           0  1922-03-02T01:00:00Z   
    17                 0            0           0  1922-02-09T01:00:00Z   
    18                 0            0           0  1922-02-09T01:00:00Z   
    19                 0            0           0  1921-02-10T01:00:00Z   
    20               NaN          NaN         NaN  1918-01-06T01:00:00Z   
    21                 0            0           0  1920-02-05T01:00:00Z   
    22                 0            0           0  1921-03-08T01:00:00Z   
    23                 0            0           0  1921-01-27T01:00:00Z   
    24                 0            0           0  1920-12-23T01:00:00Z   
    25                 0            0           0  1922-02-19T01:00:00Z   
    26                 0            0           0  1920-03-14T01:00:00Z   
    27                 0            0           0  1921-01-07T01:00:00Z   
    28                 0            0           0  1918-01-27T01:00:00Z   
    29                 0            0           0  1918-02-05T01:00:00Z   
    ...              ...          ...         ...                   ...   
    13792         0.4166           42          30  2013-04-07T17:00:00Z   
    13793         0.5588           30          38  2016-03-02T00:30:00Z   
    13794         0.4642           30          26  2017-01-04T00:00:00Z   
    13795         0.5178           27          29  2016-11-24T00:00:00Z   
    13796         0.5076           32          33  2015-02-08T20:00:00Z   
    13797         0.5076           32          33  2015-02-25T00:00:00Z   
    13798         0.5652           20          26  2015-10-18T17:00:00Z   
    13799         0.4098           36          25  2016-02-25T00:30:00Z   
    13800          0.409           39          27  2014-12-12T00:00:00Z   
    13801         0.4255           27          20  2015-01-01T00:30:00Z   
    13802         0.6349           23          40  2018-01-23T00:00:00Z   
    13803         0.5223           32          35  2014-11-12T00:00:00Z   
    13804            0.5           26          26  2013-11-10T00:00:00Z   
    13805         0.4193           36          26  2016-04-05T23:00:00Z   
    13806         0.5873           26          37  2013-03-21T23:00:00Z   
    13807         0.4363           31          24  2016-11-25T20:00:00Z   
    13808         0.4905           27          26  2017-12-23T22:00:00Z   
    13809         0.5087           28          29  2013-10-26T23:00:00Z   
    13810         0.5762           25          34  2014-11-27T00:30:00Z   
    13811          0.614           22          35  2013-02-24T00:00:00Z   
    13812         0.5074           33          34  2013-12-07T18:00:00Z   
    13813           0.48           26          24  2013-11-28T00:00:00Z   
    13814          0.551           22          27  2015-10-31T17:00:00Z   
    13815         0.6326           18          31  2018-02-11T01:00:00Z   
    13816         0.5573           27          34  2016-12-17T18:00:00Z   
    13817         0.5151           32          34  2015-02-25T00:00:00Z   
    13818         0.4426           34          27  2018-02-13T00:00:00Z   
    13819         0.3939           40          26  2015-02-25T00:00:00Z   
    13820         0.6545           19          36  2015-03-04T00:00:00Z   
    13821          0.492           32          31  2018-01-14T00:00:00Z   
    
               gameId gameLocationCode  gamesPlayed  goalsAgainst  goalsFor  \
    0      1917020002                R            1          10.0       9.0   
    1      1918020026                H            1           4.0       3.0   
    2      1919020045                R            1          11.0       6.0   
    3      1919020044                H            1           2.0      11.0   
    4      1920020023                R            1           4.0       2.0   
    5      1920020022                R            1          10.0       3.0   
    6      1920020025                H            1           5.0       6.0   
    7      1921020012                H            1           3.0       4.0   
    8      1917020011                R            1           6.0       4.0   
    9      1919020020                H            1           8.0       4.0   
    10     1920020003                H            1           4.0       5.0   
    11     1920020021                H            1           3.0       5.0   
    12     1918020001                H            1           5.0       2.0   
    13     1920020032                R            1           4.0       6.0   
    14     1920020009                H            1           5.0       1.0   
    15     1919020017                H            1           2.0       3.0   
    16     1921020044                H            1           3.0       2.0   
    17     1921020032                R            1           6.0       4.0   
    18     1921020031                H            1           1.0       9.0   
    19     1920020030                R            1           7.0       4.0   
    20     1917020036                H            1           NaN       NaN   
    21     1919020026                H            1           5.0       0.0   
    22     1920020047                R            1           6.0       4.0   
    23     1920020022                H            1           3.0      10.0   
    24     1920020002                H            1           3.0       6.0   
    25     1921020037                R            1           2.0       4.0   
    26     1919020048                R            1          11.0       4.0   
    27     1920020009                R            1           1.0       5.0   
    28     1917020018                R            1           6.0       3.0   
    29     1917020022                R            1           8.0       2.0   
    ...           ...              ...          ...           ...       ...   
    13792  2012020570                R            1           4.0       4.0   
    13793  2015020944                R            1           1.0       2.0   
    13794  2016020565                H            1           4.0       1.0   
    13795  2016020291                H            1           3.0       4.0   
    13796  2014020785                H            1           2.0       2.0   
    13797  2014020896                R            1           1.0       0.0   
    13798  2015020075                H            1           2.0       1.0   
    13799  2015020905                R            1           1.0       0.0   
    13800  2014020421                R            1           2.0       3.0   
    13801  2014020550                R            1           3.0       1.0   
    13802  2017020726                H            1           4.0       2.0   
    13803  2014020221                H            1           0.0       6.0   
    13804  2013020252                R            1           2.0       5.0   
    13805  2015021188                R            1           1.0       1.0   
    13806  2012020443                R            1           4.0       4.0   
    13807  2016020303                H            1           2.0       6.0   
    13808  2017020555                R            1           3.0       0.0   
    13809  2013020162                H            1           5.0       3.0   
    13810  2014020327                H            1           0.0       1.0   
    13811  2012020257                H            1           5.0       2.0   
    13812  2013020446                R            1           5.0       1.0   
    13813  2013020375                R            1           1.0       4.0   
    13814  2015020154                H            1           2.0       2.0   
    13815  2017020847                H            1           1.0       3.0   
    13816  2016020461                R            1           4.0       1.0   
    13817  2014020897                H            1           1.0       4.0   
    13818  2017020863                H            1           1.0       6.0   
    13819  2014020901                R            1           1.0       2.0   
    13820  2014020951                H            1           6.0       2.0   
    13821  2017020673                H            1           5.0       3.0   
    
           losses  ...  shNumTimes  shootoutGamesLost shootoutGamesWon  \
    0           1  ...           0                  0                0   
    1           1  ...           0                  0                0   
    2           1  ...           0                  0                0   
    3           0  ...           9                  0                0   
    4           1  ...           0                  0                0   
    5           1  ...           0                  0                0   
    6           0  ...           0                  0                0   
    7           0  ...           0                  0                0   
    8           1  ...           0                  0                0   
    9           1  ...           0                  0                0   
    10          0  ...           0                  0                0   
    11          0  ...           0                  0                0   
    12          1  ...           0                  0                0   
    13          0  ...           0                  0                0   
    14          1  ...           0                  0                0   
    15          0  ...           0                  0                0   
    16          1  ...           0                  0                0   
    17          1  ...           0                  0                0   
    18          0  ...           0                  0                0   
    19          1  ...           0                  0                0   
    20          0  ...         NaN                  0                0   
    21          1  ...           0                  0                0   
    22          1  ...           0                  0                0   
    23          0  ...           0                  0                0   
    24          0  ...           0                  0                0   
    25          0  ...           0                  0                0   
    26          1  ...           0                  0                0   
    27          0  ...           0                  0                0   
    28          1  ...           0                  0                0   
    29          1  ...           0                  0                0   
    ...       ...  ...         ...                ...              ...   
    13792       0  ...           3                  0                1   
    13793       0  ...           1                  0                0   
    13794       1  ...           5                  0                0   
    13795       0  ...           5                  0                0   
    13796       0  ...           4                  1                0   
    13797       1  ...           2                  0                0   
    13798       0  ...           3                  0                0   
    13799       1  ...           3                  0                0   
    13800       0  ...           2                  0                0   
    13801       1  ...           4                  0                0   
    13802       1  ...           0                  0                0   
    13803       0  ...           3                  0                0   
    13804       0  ...           6                  0                0   
    13805       0  ...           3                  0                1   
    13806       0  ...           5                  1                0   
    13807       0  ...           3                  0                0   
    13808       1  ...           2                  0                0   
    13809       1  ...           5                  0                0   
    13810       0  ...           3                  0                0   
    13811       1  ...           3                  0                0   
    13812       1  ...           5                  0                0   
    13813       0  ...           4                  0                0   
    13814       0  ...           2                  0                1   
    13815       0  ...           5                  0                0   
    13816       1  ...           3                  0                0   
    13817       0  ...           2                  0                0   
    13818       0  ...           6                  0                0   
    13819       0  ...           3                  0                0   
    13820       1  ...           1                  0                0   
    13821       1  ...           2                  0                0   
    
           shotsAgainst  shotsFor  teamAbbrev            teamFullName teamId ties  \
    0                 0         0         TAN          Toronto Arenas     57    0   
    1                 0         0         TAN          Toronto Arenas     57    0   
    2                 0         0         QBD         Quebec Bulldogs     42    0   
    3                 0         0         TSP    Toronto St. Patricks     58    0   
    4                 0         0         TSP    Toronto St. Patricks     58    0   
    5                 0         0         HAM         Hamilton Tigers     37    0   
    6                 0         0         HAM         Hamilton Tigers     37    0   
    7                 0         0         HAM         Hamilton Tigers     37    0   
    8                 0         0         MTL      Montréal Canadiens      8    0   
    9                 0         0         QBD         Quebec Bulldogs     42    0   
    10                0         0         TSP    Toronto St. Patricks     58    0   
    11                0         0         MTL      Montréal Canadiens      8    0   
    12                0         0         MTL      Montréal Canadiens      8    0   
    13                0         0         TSP    Toronto St. Patricks     58    0   
    14                0         0         HAM         Hamilton Tigers     37    0   
    15                0         0         MTL      Montréal Canadiens      8    0   
    16                0         0         HAM         Hamilton Tigers     37    0   
    17                0         0         TSP    Toronto St. Patricks     58    0   
    18                0         0         HAM         Hamilton Tigers     37    0   
    19                0         0         HAM         Hamilton Tigers     37    0   
    20              NaN       NaN         TAN          Toronto Arenas     57    0   
    21                0         0         QBD         Quebec Bulldogs     42    0   
    22                0         0         MTL      Montréal Canadiens      8    0   
    23                0         0         TSP    Toronto St. Patricks     58    0   
    24                0         0         SEN  Ottawa Senators (1917)     36    0   
    25                0         0         SEN  Ottawa Senators (1917)     36    0   
    26                0         0         MTL      Montréal Canadiens      8    0   
    27                0         0         SEN  Ottawa Senators (1917)     36    0   
    28                0         0         TAN          Toronto Arenas     57    0   
    29                0         0         SEN  Ottawa Senators (1917)     36    0   
    ...             ...       ...         ...                     ...    ...  ...   
    13792            36        34         DAL            Dallas Stars     25    0   
    13793            32        41         EDM         Edmonton Oilers     22    0   
    13794            19        25         NYR        New York Rangers      3    0   
    13795            21        25         WSH     Washington Capitals     15    0   
    13796            25        36         FLA        Florida Panthers     13    0   
    13797            29        21         CGY          Calgary Flames     20    0   
    13798            24        27         NYR        New York Rangers      3    0   
    13799            29        26         BUF          Buffalo Sabres      7    0   
    13800            34        21         CHI      Chicago Blackhawks     16    0   
    13801            28        13         NJD       New Jersey Devils      1    0   
    13802            27        31         TOR     Toronto Maple Leafs     10    0   
    13803            20        46         NYI      New York Islanders      2    0   
    13804            33        31         CHI      Chicago Blackhawks     16    0   
    13805            36        28         CAR     Carolina Hurricanes     12    0   
    13806            36        34         TOR     Toronto Maple Leafs     10    0   
    13807            36        36         MIN          Minnesota Wild     30    0   
    13808            28        26         WSH     Washington Capitals     15    0   
    13809            25        36         CHI      Chicago Blackhawks     16    0   
    13810            33        28         FLA        Florida Panthers     13    0   
    13811            39        34         CAR     Carolina Hurricanes     12    0   
    13812            34        28         PHI     Philadelphia Flyers      4    0   
    13813            26        35         STL         St. Louis Blues     19    0   
    13814            26        17         NJD       New Jersey Devils      1    0   
    13815            30        35         CAR     Carolina Hurricanes     12    0   
    13816            30        28         ARI         Arizona Coyotes     53    0   
    13817            24        35         CAR     Carolina Hurricanes     12    0   
    13818            38        22         ARI         Arizona Coyotes     53    0   
    13819            34        19         EDM         Edmonton Oilers     22    0   
    13820            30        28         VAN       Vancouver Canucks     23    0   
    13821            25        29         NJD       New Jersey Devils      1    0   
    
           wins  
    0         0  
    1         0  
    2         0  
    3         1  
    4         0  
    5         0  
    6         1  
    7         1  
    8         0  
    9         0  
    10        1  
    11        1  
    12        0  
    13        1  
    14        0  
    15        1  
    16        0  
    17        0  
    18        1  
    19        0  
    20        1  
    21        0  
    22        0  
    23        1  
    24        1  
    25        1  
    26        0  
    27        1  
    28        0  
    29        0  
    ...     ...  
    13792     1  
    13793     1  
    13794     0  
    13795     1  
    13796     0  
    13797     0  
    13798     0  
    13799     0  
    13800     1  
    13801     0  
    13802     0  
    13803     1  
    13804     1  
    13805     1  
    13806     0  
    13807     1  
    13808     0  
    13809     0  
    13810     1  
    13811     0  
    13812     0  
    13813     1  
    13814     1  
    13815     1  
    13816     0  
    13817     1  
    13818     1  
    13819     1  
    13820     0  
    13821     0  
    
    [110922 rows x 28 columns]>



## Forming the dataset

Easy peasy. Now, let's fiddle with the data.

Here, I start to think about what I want to see out of the data. Right off the bat, I see that each game played has two lines corresponding to it (one for the home team and one for the away team). I only need one side of each game to visualize data - in this case, I've decided to keep the winning side and the first side of any ties.


```python
# Creating a look up of teamId vs teamAbbrev (thought this would be useful...not so far)
teamIdLookup = set(zip(df['teamId'],df['teamAbbrev']))

# Removing all 'loss' sides of games and one side of any ties
res = pd.concat([df[df.wins==1],df[df.ties==1].drop_duplicates(subset = ['gameId','ties'], keep='first')])

# Filtering out unnecessary columns
res = res.loc[:,['gameId','gamesPlayed','teamAbbrev','opponentTeamAbbrev',
                 'goalsFor','goalsAgainst','gameLocationCode',
                 'wins', 'ties', 'shootoutGamesWon']].reset_index(drop=True)

# Create 'year' column
res['year'] = [int(str(x)[0:4]) for x in res.loc[:,'gameId']]

# Create 'seasonId' column
res['seasonId'] = [str(int(x))+'-'+str(int(x)+1) for x in res.year]

# Dropping any games with goal totals that aren't finite
res = res[np.isfinite(res.goalsFor)]

# Create 'homeScore' column which contains the score of the home team for each game
res['homeScore'] = [int(res.goalsFor[i] + (1 if res.shootoutGamesWon[i] == 1 else 0))
                    if res.gameLocationCode[i] == 'H' else int(res.goalsAgainst[i]) for i in res.index]

# Create 'roadScore' column which contains the score of the away team for each game
res['roadScore'] = [int(res.goalsFor[i] + (1 if res.shootoutGamesWon[i] == 1 else 0))
                    if res.gameLocationCode[i] == 'R' else int(res.goalsAgainst[i]) for i in res.index]


res.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>gameId</th>
      <th>gamesPlayed</th>
      <th>teamAbbrev</th>
      <th>opponentTeamAbbrev</th>
      <th>goalsFor</th>
      <th>goalsAgainst</th>
      <th>gameLocationCode</th>
      <th>wins</th>
      <th>ties</th>
      <th>shootoutGamesWon</th>
      <th>year</th>
      <th>seasonId</th>
      <th>homeScore</th>
      <th>roadScore</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1919020044</td>
      <td>1</td>
      <td>TSP</td>
      <td>QBD</td>
      <td>11.0</td>
      <td>2.0</td>
      <td>H</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1919</td>
      <td>1919-1920</td>
      <td>11</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1920020025</td>
      <td>1</td>
      <td>HAM</td>
      <td>MTL</td>
      <td>6.0</td>
      <td>5.0</td>
      <td>H</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1920</td>
      <td>1920-1921</td>
      <td>6</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1921020012</td>
      <td>1</td>
      <td>HAM</td>
      <td>MTL</td>
      <td>4.0</td>
      <td>3.0</td>
      <td>H</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1921</td>
      <td>1921-1922</td>
      <td>4</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1920020003</td>
      <td>1</td>
      <td>TSP</td>
      <td>MTL</td>
      <td>5.0</td>
      <td>4.0</td>
      <td>H</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1920</td>
      <td>1920-1921</td>
      <td>5</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1920020021</td>
      <td>1</td>
      <td>MTL</td>
      <td>SEN</td>
      <td>5.0</td>
      <td>3.0</td>
      <td>H</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1920</td>
      <td>1920-1921</td>
      <td>5</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



## Plotly magic

I chose Plotly for the interactive and HTML embedding functionality it offered over other plotting packages. It also offers me the flexibity of configuring the plot in JavaScript (should I ever get around to learning a whole lot more JS).

I'm not going to wade into the depths of the Plotly code below - I would suggest following the [tutorials and examples here](https://plot.ly/python/getting-started/) to learn to configure plots and all their features.


```python
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.widgets import GraphWidget


def plotly_heatmap(res):
    hSet = range(0,max(res.homeScore)+1)
    rSet = range(0,max(res.roadScore)+1)
    z = np.zeros((len(rSet),len(hSet)))
    t = []

    c = res.groupby(['roadScore','homeScore']).gamesPlayed.count()

    for j, r in enumerate(sorted(rSet, reverse = False)):
        for i,h in enumerate(sorted(hSet, reverse = False)):
            try:
                z[j][i] = int(c[j][i])
            except:
                pass
            hov = ("Home: "+str(i)+
                   "<br>Away: "+str(j)+
                   "<br>Count: "+str(int(z[j][i])))
            t.append(hov)

    t = [t[i:i+len(hSet)] for i in range(0, len(t), len(hSet))]


    data = [{
            'z': z,
            'type': 'heatmap',
            'colorscale': [
                [0, 'rgb(255, 255, 255)'],
                [0.0001, 'rgb(230,250,255)'],
                [0.01, 'rgb(150,200,255)'],
                [0.5, 'rgb(150,0,75)'],
                [0.8, 'rgb(120,0,75)'],
                [1., 'rgb(50, 0, 0)']],
            'colorbar': {
                'tick0': 0,
                'tickmode': 'array',
                'tickvals': [0, 500, 1000, 1500, 2000, 2500, 3000, 3500]},
            'hoverinfo':'text',
            'showscale': False,
            'text': t
            },
            go.Histogram(y = res.roadScore,
                         xaxis = 'x2',
                         marker = dict(color = 'rgba(0,0,1,.1)'),
                         hoverinfo = 'text', 
                         text = list(res.groupby('roadScore').gamesPlayed.count())), 
            go.Histogram(x = res.homeScore,
                         yaxis = 'y2',
                         marker = dict(color = 'rgba(0,0,1,.1)'),
                         hoverinfo = 'text', 
                         text = list(res.groupby('homeScore').gamesPlayed.count()))
            ]

    axesColor = 'rgb(200,200,200)'

    layout = go.Layout(
        #title='<b>NHL SCORE DISTRIBUTION</b>',
        titlefont = dict(size = 50, 
                         color = axesColor),
        xaxis = dict(ticks = list(hSet),
                     domain = [0,.8], 
                     nticks=len(hSet)+1,
                     fixedrange = True,
                     side = 'top',
                     ticklen = 0,
                     tickfont = dict(color = axesColor, size = 15),
                     title='',
                     titlefont=dict(size=18,color=axesColor)),
        yaxis = dict(ticks= list(rSet),
                     domain = [0.2,1],
                     autorange = 'reversed', 
                     fixedrange = True,
                     nticks=len(rSet)+1,
                     ticklen = 0,
                     tickfont = dict(color = axesColor, size = 15)),
        xaxis2 = dict(zeroline = False,
                      domain = [0.8,1],
                      fixedrange = True,
                      scaleratio = 10,
                      showgrid = False,
                      tickfont = dict(color = axesColor, size = 8),
                      showticklabels=False),
        yaxis2 = dict(zeroline = False,
                      domain = [0,.2],
                      autorange = 'reversed', 
                      fixedrange = True,
                      scaleratio = 10,
                      showgrid = False,
                      tickfont = dict(color = axesColor, size = 8),
                      showticklabels=False),
        annotations = [dict(x=0, y=1.11, xref = 'paper', yref = 'paper',
                            showarrow = False,
                            text = '<b>home<b>', 
                            font = dict(size=40, color = axesColor)),
                       dict(x=-0.1, y=1, xref = 'paper', yref = 'paper',
                            showarrow = False,
                            text = '<b>away<b>',
                            textangle = -90,
                            font = dict(size=40, color = axesColor))],
        showlegend = False,
        hovermode = 'closest',
#         autosize = True,
        height = 750,
        width = 800,
        margin = dict(r=0, b=0),
        )

    fig = go.Figure(data = data, layout = layout)
    
    return fig

```


    <IPython.core.display.Javascript object>



```python
fig = plotly_heatmap(res)

plot(fig, filename='scores-heatmap.html')
```




    'file://c:\\users\\madha\\Projects\\NHL Scores\\scores-heatmap.html'




```python
res2 = res.groupby(['year','seasonId']).sum()
res2.reset_index(inplace=True)
res2['avgHomeGPG'] = res2.homeScore/res2.gamesPlayed
res2['avgAwayGPG'] = res2.roadScore/res2.gamesPlayed
res2['avgHomeAwayDiff'] = res2.avgHomeGPG - res2.avgAwayGPG

traceHome = go.Bar(x = res2.seasonId, 
                   y = [round(x,2) for x in res2.avgHomeGPG], 
                   name = 'Home GpG', 
                   marker = dict(color = 'rgba(150,0,115,.7)')
                  )
traceAway = go.Bar(x = res2.seasonId, 
                       y = [round(x,2) for x in res2.avgAwayGPG],
                       name = 'Away GpG', 
                       marker = dict(color = 'rgba(0,150,200,.7)')
                      )
traceDiff = go.Scatter(x = res2.seasonId, 
                       y = [round(x,2) for x in res2.avgHomeAwayDiff], 
                       name = 'GpG Diff', 
                       marker = dict(color = 'rgba(0,0,0,1)')
                      )

data = [traceHome, traceAway, traceDiff]

fig = go.Figure(data = data)

plot(fig, filename='GPG-barplot.html')
```




    'file://c:\\users\\madha\\Projects\\NHL Scores\\GPG-barplot.html'




```python

```


```python

```
