from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH, options=op)

url = 'https://www.imdb.com/search/title/?title_type=tv_series&num_votes=1000,&genres=animation&keywords=anime&view=advancedhttps://www.imdb.com/search/title/?title_type=tv_series&num_votes=1000,&genres=animation&keywords=anime&view=advanced'

driver.get(url)
next_button_exists = True

dictionary = {} #string for movie pointing to an int for score

counter = 0

while counter < 3:

    soup = BeautifulSoup(driver.page_source, "html.parser")
    titles = soup.find_all('h3', {'class': 'lister-item-header'})
    ratings = soup.find_all('div', {'class': 'inline-block ratings-imdb-rating'})
    descriptions = soup.find_all('p', {'class':'text-muted'})
    images = soup.find_all('div', {'class': 'lister-item-image float-left'})

    processed_ratings = []
    processed_titles = []
    processed_descriptions = []
    processed_images = []

    i = 0
    while i < len(ratings):
        rating = ratings[i]
        r = rating.text
        r = r.replace('\n', '')
        processed_ratings.append(r)
        i += 1
    for title in titles:
        t = title.find('a').contents[0]
        processed_titles.append(t)
    for d in descriptions:
        d_text = d.text
        d_text = d_text.replace('\n', '')
        d_text = d_text.replace('See full summary\u00a0\u00bb', '')
        d_text = d_text.strip()
        processed_descriptions.append(d_text)
    processed_descriptions = processed_descriptions[1::2]

    print(len(images))
    for image in images:
        img = image.find('img')
        file_type = img['src'][len(img['src'])-3:]
        if file_type == 'png':
            processed_images.append(img['loadlate'])
        else:
            processed_images.append(img['src'])

    for i in range(0, len(processed_titles)):
        dictionary[processed_titles[i]] = (processed_ratings[i], 
                                            processed_descriptions[i],
                                            processed_images[i])
    
    processed_ratings = []
    processed_titles = []
    processed_descriptions = []
    
    print(counter)

    if len(driver.find_elements(By.LINK_TEXT, value='Next »')):
        next_button = driver.find_element(By.LINK_TEXT, value='Next »')
        counter += 1
        next_button.click()
    else:
        next_button_exists = False

json_obj = json.dumps(dictionary, indent=4)
with open("imdb.json", "w") as outfile:
    outfile.write(json_obj)
driver.close()