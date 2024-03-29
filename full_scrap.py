from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import importlib
from test_external_source import *
import test_external_source


#source = source.replace('"', ' ')
global article_content
article_content = []
global giant_list
giant_list = []
global nested_information  
#Get first page url, then all sequential pages, you can determine how many pages.
def next_page(your_source, part_source, div_, a_):
    print('scrapping....')
    counter = 0
    d = 1
    global next_url
    while(counter == 0):
        more_content_url = your_source.format(d)
        
        article_path = requests.get(more_content_url).text
        soup = BeautifulSoup(article_path, 'lxml')
        next_page = soup.find('div', class_=div_)
        anchor_next = next_page.find('a', class_=a_)
        next_uri = anchor_next.get('href')
        counter = 1
        d +=1
        next_url = part_source + next_uri
        second_pages(next_url, second_pages_all_url)  
        #pick how many pages you want here... 
        while (counter >= 1 and counter <= 2):
            more_content_url = your_source.format(d)
            article_path = requests.get(more_content_url).text
            soup = BeautifulSoup(article_path, 'lxml')
            next_page = soup.find('div', class_=div_)
            anchor_next = next_page.find('a', class_=a_)
            next_uri = anchor_next.get('href')
            next_url = part_source + next_uri
            #getting the link on the next button to scrape the next page in second_pages. so this step is always going to scrape the next page, not the current more_content_url page
            second_pages(next_url, second_pages_all_url)
            counter += 1
            d += 1
    to_data_frame(giant_list)
    importlib.reload(test_external_source)
    
   
    
#find all the links to the individual articles, clean them up (create_url) and put them in list second_list_uri, return the other functions aka the text file with cleaned up data.
def second_pages(link_here, div_):
    global second_list_uris
    second_list_uris = []
    article_path = requests.get(link_here).text
    soup = BeautifulSoup(article_path, 'lxml')
    all_url_tags = soup.find_all('div', class_=div_)
    for ugly_url in all_url_tags:
        anchor_url = ugly_url.a
        clean_urls=anchor_url.get('href')
        second_list_uris.append(clean_urls)
    #call all of our other functions!
    #call the function that creates a list of full urls
    create_url(second_list_uris, domain)
    #unpack url list to single url in order to open and go to single article
    single_article(all_urls, single_article_headline, single_article_author, single_article_article)
    #format the article list into text file
    #seperate_articles(article_content)
                
#create the url for the individual article    
def create_url(uri_list, landing_page):
    global all_urls
    all_urls = []
    for uri in uri_list: 
        uri = domain + uri
        all_urls.append(uri)

#go to the individual article to gather the text body, then clean it up by passing it into seperate_articles()
def single_article(enter_urls, head_, auth_, art_):
    #add to the dictionary (see top of file for global variables) to go inside a big list of all the news articles collected.  
    for url in enter_urls:
        nested_information = {"author": "", "headline":"", "article":[], 'topic':""}
        news_path = requests.get(url).text
        soup = BeautifulSoup(news_path, 'lxml')
        news_headline = soup.find('h1', class_=head_).text
        news_author_messy = soup.find('p', class_=auth_).a
        nested_information['topic'] = t
        if(news_author_messy == None):
            news_author = news_author_messy
            nested_information['author']= news_author
        else: 
            news_author = news_author_messy.text
            
            nested_information['author']= news_author
        
        news_article = soup.find_all('p', class_=art_)  
        #nested_information['headline'].append(news_headline)
        nested_information['headline'] = news_headline
        #append all the <p> tags to the individual article key value in the dictionary
        for paragraph in news_article:
            par = paragraph.text
            article_content.append(par) 
            nested_information['article'].append(par)
        giant_list.append(nested_information)
        




#change 'w' to 'a' if you want to run the program for more than one topic
def to_data_frame(data_frame):
    for news_dict in data_frame:
        formated_article= ''.join(news_dict['article'])
        news_dict['article'] = formated_article
    #print(data_frame[0])
    news_df = pd.DataFrame(data_frame)
    news_df['author'] = news_df['author'].fillna('Reuters Staff')
    #print(news_df.head(15))
    data = news_df.to_csv(index=False)
    with open('data_frame.csv', 'a') as f:
        f.write(data)
    






if __name__ == '__main__':
    #as propmted and notified from user_input(), 4 is to quit()
    while True:
        next_page(source, source_uri, div_next_page, a_next_page)
        







 
