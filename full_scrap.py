from bs4 import BeautifulSoup
import requests
import time
import re


def article_url():
    #took the global from single_article (article_content) to test the bug of empty array
    global article_content
    article_content = []
    global list_uris
    list_uris = []
    global next_url_snippet 
    next_url_snippet = []
    article_path = requests.get('https://www.reuters.com/news/archive/worldnews?view=page&page=1&pageSize=10').text
    soup = BeautifulSoup(article_path, 'lxml')
    all_url_tags = soup.find_all('div', class_='story-content')
    for ugly_url in all_url_tags:
        anchor_url = ugly_url.a
        clean_urls=anchor_url.get('href')
        list_uris.append(clean_urls)
    #call all of our other functions!
    create_url(list_uris)
    #^^ call the function that creates a list of full urls
    single_article(all_urls)
    #seperate_articles(article_content) #***** placed this in single_article
    #get the next page. Need to work on this to set it up for infinate loop
    #next_page()
    #second_pages(next_url)

def second_pages(link_here):
    global second_list_uris
    second_list_uris = []
    article_path = requests.get(link_here).text
    soup = BeautifulSoup(article_path, 'lxml')
    all_url_tags = soup.find_all('div', class_='story-content')
    for ugly_url in all_url_tags:
        anchor_url = ugly_url.a
        clean_urls=anchor_url.get('href')
        second_list_uris.append(clean_urls)
    #call all of our other functions!
    create_url(second_list_uris)
    #^^ call the function that creates a list of full urls
    single_article(all_urls)
    seperate_articles(article_content)
    
     

       
#create the url for the individual article    
def create_url(uri_list):
    global all_urls
    all_urls = []
    for uri in uri_list: 
        uri = 'https://www.reuters.com/' + uri
        all_urls.append(uri)


        
def single_article(enter_urls):

    for url in enter_urls:
        news_path = requests.get(url).text
        soup = BeautifulSoup(news_path, 'lxml')
        news_article = soup.find_all('p', class_='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
        for paragraph in news_article:
            par = paragraph.text
            article_content.append(par)
    seperate_articles(article_content)
    #get the next page url of THIS current page!

            

        
def seperate_articles(article_body):
    joined_articles = " ".join(article_body)
    parsed_list = joined_articles.split(' (Reuters)')
    with open('articles/news_art.txt', 'w') as f:
        for item in parsed_list:
            f.write("%s\n" % item)

#Get url for the next page of 10 results
def next_page():
    #************* try to make it so it will not revert back to home page
    #article_path = requests.get('https://www.reuters.com/world').text

    more_content_url = 'https://www.reuters.com/news/archive/worldnews?view=page&page=1&pageSize=10'
    article_path = requests.get(more_content_url).text
    soup = BeautifulSoup(article_path, 'lxml')
    next_page = soup.find('div', class_="control-nav")
    anchor_next = next_page.find('a', class_="control-nav-next")
    next_uri = anchor_next.get('href')
    #create url
    global next_url
    next_url = 'https://www.reuters.com/news/archive/worldnews' + next_uri

    second_pages(next_url)
    
""" def next_page_url(current_page):
    global more_articles_url
    more_articles_url = []
    for uri in current_page:
        uri = current_page + uri
        more_articles_url.apprend(uri)   """ 
#^^ how to get the current page url and add 1 to the page=# section to trigger the next page search??

article_url()
next_page()






 
""" if __name__ == '__main__':
    while True:
        #set up a for loop
        article_url()
        second_pages(next_url)
        time_wait = 5
        print(f'waiting {time_wait} minutes....')
        time.sleep(time_wait * 60)   """