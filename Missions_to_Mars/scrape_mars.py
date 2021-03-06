#!/usr/bin/env python
# coding: utf-8

# In[19]:


#import dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo


# In[35]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[62]:


def scrape_all():
    news_tite, news_p = mars_news()
    featured_img_url = featured_image()
    mars_facts_html = mars_facts()
    full_img_list = hemisphere_data()

    nasa_document = {
        'news_title': news_tite,
        'news_paragraph': news_p,
        'featured_img_url': featured_img_url,
        'mars_facts_html': mars_facts_html,
        'hemisphere_img_list': full_img_list
    }

    
    #consider closeing browser here
    browser.quit()
    
    
    return nasa_document


# # NASA Mars News



# In[47]:


def mars_news():
    # URL of page to be scraped
    url = ('https://mars.nasa.gov/news/')

    # Retrieve page with the browser module
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # save the most recent article, title and date
    article = news_soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    #print(news_date)
    #print(news_title)
    #print(news_p)
    
    return news_title, news_p


# # JPL Mars Space Images - Featured Image

# In[52]:


def featured_image():

    #Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # URL of page to be scraped
    url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # Retrieve page with the browser module
    browser.visit(url)

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    
    #find the image url for the current Featured Mars Image
    image_url = image_soup.find("a", class_="fancybox")['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url
    #print(featured_image_url)
    
    return featured_image_url


# # Mars Facts

# In[50]:



def mars_facts():
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    mars_facts_df = pd.read_html(url)
    mars_facts_df = mars_facts_df[0]
    mars_facts_df.columns = ['Description', 'Mars']
    mars_facts_df.set_index('Description', inplace = True)
    mars_facts_df

    mars_data_html = mars_facts_df.to_html(classes='table table-striped')
    
    return mars_data_html


# # Mars Hemispheres

# In[34]:


def hemisphere_data():

    #Visit the USGS Astrogeology site 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')

    #loop thru the links to the hemispheres to find the image url to the full resolution image
    #add each 'title' and 'img_url' to a list
    results = hemisphere_soup.find_all("div", class_="item")

    hemisphere_list = []
    for result in results:

        title = result.find("h3").text
        href = result.find("a", class_= 'itemLink')['href']
        img_url = 'https://astrogeology.usgs.gov' + href
        hemisphere_list.append({'title' : title, 'img_url' : img_url})

    #define full img list
    full_img_list = []

    #loop through url's of hemisphere_list and parse through html to find full_img_url
    for hemisphere_dict in hemisphere_list:

        url = hemisphere_dict['img_url']

        browser.visit(url)
        html = browser.html
        hemisphere_soup = BeautifulSoup(html, 'html.parser')

        results = hemisphere_soup.find_all("div", class_="downloads")

        for result in results:

            hemisphere_title = hemisphere_dict['title']
            full_hemisphere_img = result.find("a")['href']    

            full_img_list.append({'title' : hemisphere_title, 'img_url' : full_hemisphere_img})

    return full_img_list

# # Mongo DB



# In[64]:

# run script
if __name__ == '__main__':
    scrape_all()
        




# In[ ]:




