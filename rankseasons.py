import requests
import datetime
import time
import pandas
import matplotlib.pyplot as plt

seasons = ['WINTER', 'SPRING', 'SUMMER', 'FALL']

url = 'https://graphql.anilist.co'


def seasonal_rankings_one_season(year, season, page):

    query = '''
    query ($year:Int, $season:MediaSeason, $page:Int) {
        Page(page: $page) {
            pageInfo {
                hasNextPage
            }
            media (season: $season, seasonYear:$year){
                type
                averageScore
            }
        }
    }'''

    variables = {
        'year': year,
        'season':season,
        'page':page
    }

    response = requests.post(url, json={'query': query, 'variables': variables}).json()
    
    hasNextPage = response['data']['Page']['pageInfo']['hasNextPage']

    listOfScores = []

    for anime in response['data']['Page']['media']:
        if anime['type'] == 'ANIME' and anime['averageScore'] is not None:
            listOfScores.append(anime['averageScore'])

    if hasNextPage:
        newListOfScores = seasonal_rankings_one_season(year, season, page+1)
        listOfScores += newListOfScores
        
    return listOfScores


def findBestSeason(startYear):
    dictOfScores = {'WINTER':[], 'SPRING':[], 'SUMMER':[], 'FALL':[]}
    while startYear < datetime.datetime.now().year:
        for season in seasons:
            dictOfScores[season] += seasonal_rankings_one_season(startYear, season, 1)
            time.sleep(5)
        startYear += 1
    return dictOfScores    

dictOfScores = findBestSeason(2010)
dfWinter = pandas.DataFrame(dictOfScores['WINTER'], columns=['WINTER'])
dfSpring = pandas.DataFrame(dictOfScores['SPRING'], columns=['SPRING'])
dfSummer = pandas.DataFrame(dictOfScores['SUMMER'], columns=['SUMMER'])
dfFall = pandas.DataFrame(dictOfScores['FALL'], columns=['FALL'])

print(dfWinter.describe())
print(dfSpring.describe())
print(dfSummer.describe())
print(dfFall.describe())