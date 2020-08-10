#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

#get_ipython().system('which chromedriver')


# Setting up chrome browser for splinter
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless = True)


def scrape_info():
    browser = init_browser()
    # ## Mars News

    # URL of page to be scraped and broswer visiting URL
    mars_news = "https://mars.nasa.gov/news/"
    browser.visit(mars_news)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    # Finding news heading and para on site
    title_news = soup.find_all('div', class_="content_title")
    para = soup.find_all('div', class_="article_teaser_body")

    # Storing first news and para in variables
    news_title = title_news[1].text
    news_p = para[0].text

    # Setting up url for browser to visit
    feat_img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(feat_img_url)
    time.sleep(1)

    # Clicking on full image by browser to get source of full image
    browser.click_link_by_id('full_image')
    time.sleep(1)

    # Browser visiting site
    html = browser.html
    soup = bs(html, "html.parser")

    # Image source scrapping and finalizing final image link
    image_url = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    # Setting up url for browser to visit
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(1)

    # Prepareing borwser for scrapping
    html = browser.html
    soup = bs(html, "html.parser")

    # Defining results to store scrapped data from relevent divs
    results = soup.find_all('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-1mi0q7o')

    # Storing scrapped data in a list
    tweets = []

    # First loop to run through all the divs
    for res in results:
        re = res.find_all('div', class_='css-1dbjc4n')
        # Second loop for furhter narrowing of data
        for r in re:
            try: 
                text = r.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
                # Appending data to list which contains on certain elements in text
                if ("sol" or "Sol" or "InSight") in text:
                    tweets.append(text)
            except AttributeError as e:
                e

    # Getting the first tweet from the scrapped data
    mars_weather = tweets[0]

    # Setting up url for pandas scrapping
    facts_url = 'https://space-facts.com/mars/'

    # Extracting table from site
    tables = pd.read_html(facts_url)

    # Getting first data from site and converting the table to html
    df = tables[0]
    mars_df = df.rename(columns = {0: 'Details', 1: 'Values'})
    mars_df = mars_df.set_index('Details')
    mars_table_html = mars_df.to_html(header = True)
    # Removing '\n' from html code
    mars_table_html = mars_table_html.replace('\n','')

    # Setting up url for browser to scrap and visit
    mars_images_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_images_url)
    time.sleep(1)

    # preparing beautiful soup for scrapping
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrapping small images data
    img_m = soup.find_all('div', class_='item')

    # Defining dictionary for storining final data
    hemisphere_image_urls = []

    # For loop to run through dictionary
    for img in img_m:
        # Getting image link and creating full url for browser to visit
        img_link = img.a['href']
        img_visit_url = f'https://astrogeology.usgs.gov{img_link}'
        
        # Broswer visitin full url
        browser.visit(img_visit_url)
        html = browser.html
        soup = bs(html, "html.parser")
        
        # Scrapping data from visited links full-image src and heading 
        img_short_url = soup.find('img', class_='wide-image')['src']
        img_full_url = f'https://astrogeology.usgs.gov{img_short_url}'
        heading = soup.find('h2', class_='title').text
        # Removing word enhanced in the end of heading
        heading = heading.rsplit(' ', 1)[0]
        
        # Creating dictionary of title and image url and appending data to list
        img_dict = {"title": heading, "img_url": img_full_url}
        hemisphere_image_urls.append(img_dict)

    # Storing final scrapped variables in a dictionary for website connection
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_table_html':mars_table_html,
        'hemisphere_image_urls':hemisphere_image_urls
    } 

    browser.quit()

    return mars_data
