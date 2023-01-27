import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import openpyxl

# Initialize the webdriver
# driver = webdriver.Chrome()
#
# # Open the website in the browser
# driver.get("https://twitter.com/i/trends")
#
# # Wait for the page to fully load
# time.sleep(20)
#
# # Get the HTML source code of the page
# html = driver.page_source
#
# # Use BeautifulSoup to parse the HTML
# soup = BeautifulSoup(html, "html.parser")
#
# # source = soup.find_all('div', attrs={'class':  'css-901oao r-1awozwy r-1nao33i r-6koalj r-37j5jr r-adyw6z r-1vr29t4 r-135wba7 r-bcqeeo r-1udh08x r-qvutc0'})
# # print(source)
# # Print the HTML source code
# print(soup.prettify())
#
# # Close the browser
# driver.close()


def get_html_source():
    url = "https://twitter.com/i/trends"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    return soup


class TwitterScraping:

    def __init__(self):
        self.soup = get_html_source()

    def get_trends(self):
        soup = self.soup
        trends = soup.find('div', attrs={
            'class': 'css-1dbjc4n'}).find_all('div', attrs={'class': 'css-1dbjc4n r-16y2uox r-bnwqim'})
        return trends

    def get_titles(self):
        trends = self.get_trends()
        trend_title = list(map(lambda trend: trend.contents[0].text, trends))
        print("count trend_title", len(trend_title))

        return trend_title

    def get_names(self):
        trends = self.get_trends()
        trend_names = list(map(lambda trend: trend.contents[1].text, trends))
        print("count names", len(trend_names))
        return trend_names

    def get_twit_count(self):
        trends = self.get_trends()
        trend_count = list(map(lambda trend: trend.contents[2].text, trends))
        trend_counts = [trend.contents[2].text for trend in trends]
        print("count twit ",len(trend_counts))

        return trend_count

    def save_excel(self):
        twit_titles = self.get_titles()
        twit_names = self.get_names()
        twit_counts = self.get_twit_count()

        index = [i for i in range(1, len(twit_titles) + 1)]
        print(index)

        df = pd.DataFrame(list(zip(index, twit_titles, twit_names, twit_counts)),
                          columns=['twit sırası', 'gündem başlığı', 'Gündem', 'Atılan Twit'])
        print(df)
        df.to_excel('twitter-trend.xlsx', sheet_name='twitter-trend')


twitter = TwitterScraping()
#
# print(twitter.get_titles())
# print(twitter.get_names())
print(twitter.get_twit_count())
print(twitter.save_excel())


