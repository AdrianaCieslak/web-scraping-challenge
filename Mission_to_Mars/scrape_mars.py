from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

    
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    data = {
        "news_title": news_title,
        "news_paragraph": news_para,
        "featured_image": featured_image_url(browser),
        "mars_facts": table(),
        "facts": mars_facts(),
        "hemisphere_images": hemisphere_image_urls(browser)
        
    }

    browser.quit()
    return data

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    title = soup.find_all("div", class_="content_title")
    title[1].text
    para = soup.find_all("div", class_="article_teaser_body")
    para[0].text
    news_title = title[1].text
    news_para = para[0].text
    return news_title, news_paragraph

def featured_image(browser):
    base = "https://www.jpl.nasa.gov"
    url = f"{base}/spaceimages/?search=&category=Mars"
    browser.visit(url) 
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    soup.find_all("div", class_="download_tiff")[1].select("a")[0].get("href")
    new_image = soup.find_all("div", class_="download_tiff")[1].select("a")[0].get("href")
    featured_image_url = f"https:{new_image}"
    return featured_image_url

def mars_facts():
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    df = table[0]
    df.columns = ['Facts', 'Values']
    df = df.iloc[1:]
    df.set_index('Facts', inplace=True)
    html_table = df.to_html(index=True, header=True)
    return html_table

def hemispheres():
    url = 'https://astrogeology.usgs.gov'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for result in results:
    
        title= result.find('h3').text
        link = result.find('a')['href']
        browser.visit(url + link)
        html = browser.html
        soup2 = bs(html, 'html.parser')
        image = soup2.find_all('div', class_='downloads')
        image_url = image[0].find_all('a')[1].get('href')
        hemisphere_image_urls.append({'title': title, 'image_url': image_url})
    return hemisphere_image_urls


if __name__ == "__main__":
    scrape()