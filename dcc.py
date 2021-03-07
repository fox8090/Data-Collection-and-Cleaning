from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import csv


def getArticles(query):
    url = 'https://www.bbc.co.uk/search?q=' + query + '&page='
    page = 1
    articleLinks = [] 
    flag = False
    while len(articleLinks) != 100:
        try:
            response = requests.get(url + str(page))
            response.raise_for_status()
        except HTTPError as http_err:
            print('HTTP ERROR OCCURRED ACCESSING '+ url + str(page) + ': ', http_err)
            exit()
        except Exception as err:
            print('OTHER ERROR OCCURRED ACCESSING '+ url + str(page)+ ': ', err)
            exit()
        else:
            text = BeautifulSoup(response.text, 'html.parser')
        for link in text.find_all('a'):
            item = link.get('href')
            if item in articleLinks or len(articleLinks) == 100:
                flag = True
                break
            if ('www.bbc.co.uk/news/' in item or 'news.bbc.co.uk/' in item) and not('/localnews' in item) and not('/help' in item):
                articleLinks.append(item)
        if flag:
            break
        page += 1
    print(articleLinks, len(articleLinks))
    #return articleLinks

query = 'Advanced Persistent Threat'
getArticles(query)


with open(query+'_articles.csv', mode='w') as theFile:
    writer = csv.DictWriter(theFile, ['url', 'content'])
    


