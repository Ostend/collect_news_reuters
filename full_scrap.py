from bs4 import BeautifulSoup
import requests
import time
import re
import json
#Get first page url, then all sequential pages, you can determine how many pages.
def next_page():
    global article_content
    article_content = []
    counter = 0
    d = 1
    global next_url
    while(counter == 0):
        more_content_url = 'https://www.reuters.com/news/archive/worldnews?view=page&page={}&pageSize=10'.format(d)
        article_path = requests.get(more_content_url).text
        soup = BeautifulSoup(article_path, 'lxml')
        next_page = soup.find('div', class_="control-nav")
        anchor_next = next_page.find('a', class_="control-nav-next")
        next_uri = anchor_next.get('href')
        counter = 1
        d +=1
        next_url = 'https://www.reuters.com/news/archive/worldnews' + next_uri
        second_pages(next_url)   
        while (counter >= 1 and counter <= 2):
            more_content_url = 'https://www.reuters.com/news/archive/worldnews?view=page&page={}&pageSize=10'.format(d)
            article_path = requests.get(more_content_url).text
            soup = BeautifulSoup(article_path, 'lxml')
            next_page = soup.find('div', class_="control-nav")
            anchor_next = next_page.find('a', class_="control-nav-next")
            next_uri = anchor_next.get('href')
            next_url = 'https://www.reuters.com/news/archive/worldnews' + next_uri
            #getting the link on the next button to scrape the next page in second_pages. so this step is always going to scrape the next page, not the current more_content_url page
            second_pages(next_url)
            counter += 1
            d += 1
    
#find all the links to the individual articles, clean them up (create_url) and put them in list second_list_uri, return the other functions aka the text file with cleaned up data.
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
    #call the function that creates a list of full urls
    create_url(second_list_uris)
    #unpack url list to single url in order to open and go to single article
    single_article(all_urls)
    #format the article list into text file
    #seperate_articles(article_content)
                
#create the url for the individual article    
def create_url(uri_list):
    global all_urls
    all_urls = []
    for uri in uri_list: 
        uri = 'https://www.reuters.com/' + uri
        all_urls.append(uri)

#go to the individual article to gather the text body, then clean it up by passing it into seperate_articles()
def single_article(enter_urls):
    global giant_list
    giant_list = []
    global nested_information  
    #create a dictionary to go inside a big list of all the news articles collected.  
    for url in enter_urls:
        nested_information = {"author": [], "headline":[], "article":[]}
        news_path = requests.get(url).text
        soup = BeautifulSoup(news_path, 'lxml')
        news_headline = soup.find('h1', class_='Headline-headline-2FXIq Headline-black-OogpV ArticleHeader-headline-NlAqj').text
        news_author_messy = soup.find('p', class_='Byline-byline-1sVmo ArticleBody-byline-10B7D').a
        
        if(news_author_messy == None):
            news_author = news_author_messy
            nested_information['author'].append(news_author)
        else: 
            news_author = news_author_messy.text
            
            nested_information['author'].append(news_author)
        
        news_article = soup.find_all('p', class_='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')  
        nested_information['headline'].append(news_headline)
        #nested_information['author'].append(news_author)
        #append all the <p> tags to the individual article key value in the dictionary
        for paragraph in news_article:
            par = paragraph.text
            article_content.append(par) 
            nested_information['article'].append(par)
        giant_list.append(nested_information)
        #print(len(giant_list))
    #seperate_articles(article_content)
    dict_file(giant_list)


def dict_file(organized_list):
    with open('append_articles.txt', 'a') as f:
        json.dump(organized_list, f)
    
    

next_page()




 
""" if __name__ == '__main__':
    while True:
        #set up a for loop
        article_url()
        second_pages(next_url)
        time_wait = 5
        print(f'waiting {time_wait} minutes....')
        time.sleep(time_wait * 60)   """