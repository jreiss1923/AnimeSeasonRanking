import requests
import datetime
import time

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
                popularity
            }
        }
    }'''

    variables = {
        'year': year,
        'season':season,
        'page':page
    }

    response = requests.post(url, json={'query': query, 'variables': variables}).json()
    print(response)
    
    hasNextPage = response['data']['Page']['pageInfo']['hasNextPage']

    sumOfPopularity = 0
    weightedAverageNoDivide = 0

    for anime in response['data']['Page']['media']:
        if anime['type'] == 'ANIME' and anime['averageScore'] is not None:
            sumOfPopularity += anime['popularity']
            weightedAverageNoDivide += anime['popularity'] * anime['averageScore']

    if hasNextPage:
        weightedAverageNoDivideNext, sumOfPopularityNext = seasonal_rankings_one_season(year, season, page+1)
        weightedAverageNoDivide += weightedAverageNoDivideNext
        sumOfPopularity += sumOfPopularityNext
        
    return weightedAverageNoDivide, sumOfPopularity


def findBestSeason(startYear):
    seasonDict = {"WINTER":{"weightAvg":0, "popSum":0}, "SPRING":{"weightAvg":0, "popSum":0}, "SUMMER":{"weightAvg":0, "popSum":0}, "FALL":{"weightAvg":0, "popSum":0}}
    while startYear < datetime.datetime.now().year:
        for season in seasons:
            weightAvg, popSum = seasonal_rankings_one_season(startYear, season, 1)
            seasonDict[season]["weightAvg"] += weightAvg
            seasonDict[season]["popSum"] += popSum
            time.sleep(5)
        startYear += 1
    return seasonDict     

seasonDict = findBestSeason(2010)

for season in seasonDict:
    print(season + ": " + str(seasonDict[season]['weightAvg']/seasonDict[season]['popSum']))