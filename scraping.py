from selenium import webdriver
from collections import defaultdict
import chromedriver_binary
from bs4 import BeautifulSoup
import time

link_list = defaultdict(list)

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

for i in range(1):
    url = 'https://www.nhk.or.jp/school/keyword/?kyoka=rika&grade=g5&cat=all&from={}&sort=ranking'.format(i)
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    
    for link in soup.select('div.itemKyouka > a'):
        
        mov_url = 'https:' + link.get('href')
        driver.get(mov_url)
        mov_html = driver.page_source.encode('utf-8')
        mov_soup = BeautifulSoup(mov_html, "html.parser")
        
        og_title = mov_soup.find('meta', attrs={'property': 'og:title', 'content': True})
        og_description = mov_soup.find('meta', attrs={'property': 'og:description', 'content': True})
        og_image = mov_soup.find('meta', attrs={'property': 'og:image', 'content': True})

        link_list[mov_url] += [og_title['content'], og_description['content'], og_image['content']]
        
        time.sleep(1)
    time.sleep(1)
for link, og in link_list.items():
    print(link)
    print(og)
    
