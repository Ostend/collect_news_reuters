from bs4 import BeautifulSoup
import requests
import time
import re


def article_url():
    global list_uris
    list_uris = []
    article_path = requests.get('https://www.reuters.com/world').text
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
    seperate_articles(article_content)
    #get the next page. Need to work on this to set it up for infinate loop
    next_page()
    second_pages(next_url)

def second_pages(link_here):
    global list_uris
    list_uris = []
    article_path = requests.get(link_here).text
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
    seperate_articles(article_content)
     

       
        
def create_url(uri_list):
    global all_urls
    all_urls = []
    for uri in uri_list: 
        uri = 'https://www.reuters.com/' + uri
        all_urls.append(uri)
        
def single_article(enter_urls):
    global article_content
    article_content = []
    for url in enter_urls:
        news_path = requests.get(url).text
        soup = BeautifulSoup(news_path, 'lxml')
        news_article = soup.find_all('p', class_='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
        for paragraph in news_article:
            par = paragraph.text
            article_content.append(par)
            

        
def seperate_articles(article_body):
    joined_articles = " ".join(article_body)
    parsed_list = joined_articles.split(' (Reuters)')
    with open('articles/news.txt', 'w') as f:
        for item in parsed_list:
            f.write("%s\n" % item)
    
def next_page():
    article_path = requests.get('https://www.reuters.com/world').text
    soup = BeautifulSoup(article_path, 'lxml')
    next_page = soup.find('div', class_="control-nav")
    anchor_next = next_page.find('a', class_="control-nav-next")
    next_uri = anchor_next.get('href')
    #create url
    global next_url
    next_url = 'https://www.reuters.com/' + next_uri
    
    


article_url()






 

""" if __name__ == '__main__':
    while True:
        article_url()
        
        time_wait = 5
        print(f'waiting {time_wait} minutes....')
        time.sleep(time_wait * 60)  """