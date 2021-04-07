from bs4 import BeautifulSoup
import requests
import time
import re

#Get first page url, then all sequential pages, you can determine how many pages.
def next_page():
    global article_content
    article_content = []
    #************* try to make it so it will not revert back to home page
    #article_path = requests.get('https://www.reuters.com/world').text
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
        while (counter >= 1 and counter <= 3):
            more_content_url = 'https://www.reuters.com/news/archive/worldnews?view=page&page={}&pageSize=10'.format(d)
            article_path = requests.get(more_content_url).text
            soup = BeautifulSoup(article_path, 'lxml')
            next_page = soup.find('div', class_="control-nav")
            anchor_next = next_page.find('a', class_="control-nav-next")
            next_uri = anchor_next.get('href')
           # d += 1
            next_url = 'https://www.reuters.com/news/archive/worldnews' + next_uri
            second_pages(next_url)
            counter += 1
            d += 1

#find all the links to the individual articles, clean them up (create_url) and put them in list second_list_uri
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

#go to the individual article to gather the text body, then clean it up by passing it into seperate_articles()
def single_article(enter_urls):

    for url in enter_urls:
        news_path = requests.get(url).text
        soup = BeautifulSoup(news_path, 'lxml')
        news_article = soup.find_all('p', class_='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
        for paragraph in news_article:
            par = paragraph.text
            article_content.append(par)
    seperate_articles(article_content)


#needs work, but it cleans up the list of <p> tags where the articles are broken up into and combines them, then parses them back into their individual articles into a list. Then writes them to a file.                    
def seperate_articles(article_body):
    joined_articles = " ".join(article_body)
    parsed_list = joined_articles.split(' (Reuters)')
    with open('articles/news_art.txt', 'w') as f:
        for item in parsed_list:
            f.write("%s\n" % item)






next_page()






 
""" if __name__ == '__main__':
    while True:
        #set up a for loop
        article_url()
        second_pages(next_url)
        time_wait = 5
        print(f'waiting {time_wait} minutes....')
        time.sleep(time_wait * 60)   """