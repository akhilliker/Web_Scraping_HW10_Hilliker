# import necessary libraries
from flask import Flask, render_template
import os
import requests
from bs4 import BeautifulSoup as bs
import time
from splinter import Browser
import pandas as pd
from selenium import webdriver

def sele_driver():
        driver = webdriver.Chrome()
        return driver

def init_browser():
        executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
        return Browser('chrome', **executable_path, headless = False)

def scrape():
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(3)
        html = browser.html
        soup = bs(html, 'html.parser')

        # Capture the latest headline and it's paragraph, more complete notation in jupyter notebook file
        news_title = soup.find_all('h3')
        latest_news_title = news_title[0].find(text = True)    
        news_p = soup.find_all('div', class_="rollover_description_inner")
        latest_news_p = news_p[0].find(text = True)

        # Going back through to add elements to build data into one dictionary
        mars_data = {}
        mars_data['latest_news_title'] = latest_news_title
        mars_data['news_description'] = latest_news_p
        mars_data

        # # Find Featured Image
        url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url2)
        time.sleep(3)
        html2 = browser.html
        soup2 = bs(html2, 'html.parser')

        # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
        base_url = "https://www.jpl.nasa.gov/"
        image_path = soup2.find("a", class_="button fancybox")["data-fancybox-href"]
        image_path # prints '/spaceimages/images/mediumsize/PIA16220_ip.jpg'
        featured_image_url = base_url + image_path
        featured_image_url 
        mars_data["featured_image"] = featured_image_url

        # Latest Mars Tweet
        url3 = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url3)
        time.sleep(3)
        html = browser.html
        soup3 = bs(html, 'html.parser')
        mars_tweet = soup3.find_all('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        mars_weather = mars_tweet[0].find(text = True)
        mars_data["mars_weather_tweet"] = mars_weather

        # Use Pandas to Scrape Mars Facts from Web
        url4 = 'https://space-facts.com/mars/'
        tables = pd.read_html(url4)
        mars_df = tables[0]
        mars_df.columns = ['description', 'value']
        mars_html_table = mars_df.to_html()
        mars_html_table = mars_html_table.replace('\n', "")
        mars_html_table = mars_df.to_html('mars_table.html')

        # Mars Hemispheres names and links
        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url5)
        time.sleep(3)
        html = browser.html
        soup5 = bs(html, 'html.parser')
        base_url5 = "https://astrogeology.usgs.gov"
        hemi_image_titles = []
        img_urls = []
        hemi_urls = []
        hemi_full_url = ""

        driver = sele_driver()
        driver.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

        # These are the links to click to get to the high res photo...  not the link to the photos themselves
        # Cerberus
        for a in driver.find_elements_by_xpath('//*[@class="collapsible results"]/div[1]/div/a'):
                cere_url = a.get_attribute('href')
                hemi_urls.append(cere_url)
        # Schiaparelli
        for a in driver.find_elements_by_xpath('//*[@class="collapsible results"]/div[2]/div/a'):
                schia_url = a.get_attribute('href')
                hemi_urls.append(schia_url)
        # Syrtis Major
        for a in driver.find_elements_by_xpath('//*[@class="collapsible results"]/div[3]/div/a'):
                syr_url = a.get_attribute('href')
                hemi_urls.append(syr_url)
        # Valles Marineris
        for a in driver.find_elements_by_xpath('//*[@class="collapsible results"]/div[4]/div/a'):
                val_url = a.get_attribute('href')
                hemi_urls.append(val_url)

        # Find the hemisphere titles and the links to the high res photos; save each in a list
        hemi_image_titles = []
        img_urls = []
        hemisphere_image_urls = []

        # Cerberus
        browser.visit(url5)
        cere_link_click = browser.find_by_xpath("//*[@class='collapsible results']/div[1]/div/a").click()
        browser.visit(cere_url)
        html = browser.html
        soup6 = bs(html, 'html.parser')
        cere_img_title = soup6.find("h2", class_="title").text.strip() # Give Cerberus Hemisphere Enhanced
        cere_title = cere_img_title[:-9]
        hemi_image_titles.append(cere_title)
        driver.get(cere_url)
        for b in driver.find_elements_by_xpath('//*[@id="wide-image"]/div/img'):
                cere_img_url = b.get_attribute('src')
                img_urls.append(cere_img_url)
        cere_dict = {'title' : cere_title, 'img_url' : cere_img_url}
        hemisphere_image_urls.append(cere_dict)

        # Schiaparelli 
        browser.visit(url5)
        schia_link_click = browser.find_by_xpath("//*[@class='collapsible results']/div[2]/div/a").click()
        browser.visit(schia_url)
        html = browser.html
        soup6 = bs(html, 'html.parser')
        schia_img_title = soup6.find("h2", class_="title").text.strip() # Give Cerberus Hemisphere Enhanced
        schia_title = schia_img_title[:-9]
        hemi_image_titles.append(schia_title)
        driver.get(schia_url)
        for b in driver.find_elements_by_xpath('//*[@id="wide-image"]/div/img'):
                schia_img_url = b.get_attribute('src')
                img_urls.append(schia_img_url)
        schia_dict = {'title' : schia_title, 'img_url' : schia_img_url}
        hemisphere_image_urls.append(schia_dict)

        # Syrtis Major 
        browser.visit(url5)
        syr_link_click = browser.find_by_xpath("//*[@class='collapsible results']/div[3]/div/a").click()
        browser.visit(syr_url)
        html = browser.html
        soup6 = bs(html, 'html.parser')
        syr_img_title = soup6.find("h2", class_="title").text.strip() # Give Cerberus Hemisphere Enhanced
        syr_title = syr_img_title[:-9]
        hemi_image_titles.append(syr_title)
        driver.get(syr_url)
        for b in driver.find_elements_by_xpath('//*[@id="wide-image"]/div/img'):
                syr_img_url = b.get_attribute('src')
                img_urls.append(syr_img_url)
        syr_dict = {'title' : syr_title, 'img_url' : syr_img_url}
        hemisphere_image_urls.append(syr_dict)

        # Valles Marineris 
        browser.visit(url5)
        val_link_click = browser.find_by_xpath("//*[@class='collapsible results']/div[4]/div/a").click()
        browser.visit(val_url)
        html = browser.html
        soup6 = bs(html, 'html.parser')
        val_img_title = soup6.find("h2", class_="title").text.strip() # Give Cerberus Hemisphere Enhanced
        val_title = val_img_title[:-9]
        hemi_image_titles.append(val_title)
        driver.get(val_url)
        for b in driver.find_elements_by_xpath('//*[@id="wide-image"]/div/img'):
                val_img_url = b.get_attribute('src')
                img_urls.append(val_img_url)
        val_dict = {'title' : val_title, 'img_url' : val_img_url}
        hemisphere_image_urls.append(val_dict)

        # Merge this dictionary with the one with the previous scrapped info
        mars_data["hemisphere_img_url"] = hemisphere_image_urls
        return mars_data


