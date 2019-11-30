from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time, re, math, csv, json
from bs4 import BeautifulSoup as soup  # HTML data structure

from tqdm import tqdm

from selenium.webdriver.common.keys import Keys
from nameparser import HumanName as hn
from pandas.core.common import flatten

import proxy_manager as pm
import shadow_useragent, demjson 
ua = shadow_useragent.ShadowUserAgent()
ua.random
# Create an instance of our proxy manager
proxy_scrape = pm.ProxyManager('http://google.com', ua.random)

# Refresh the status of the proxies we pulled on initialization
proxy_scrape.refresh_proxy_status()

# Get a single working proxy
proxy = proxy_scrape.get_proxy()

# Make a fresh scrape of free-proxy-list.net
proxy_scrape.update_proxy_list()

def create_browser(proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server={}'.format(proxy))
    return webdriver.Chrome(options=options)

driver = webdriver.Chrome("C:\\Users\\Administrator\\chromedriver.exe")
driver = create_browser("92.114.234.206:53999")
driver.get('https://edmundmartin.com')


hudsonville_url = "https://www.manta.com/mb_51_ALL_9NN/hudsonville_mi"
zeeland_url = "https://www.manta.com/mb_51_ALL_A1E/zeeland_mi"
grandville_url = "https://www.manta.com/mb_51_ALL_9LR/grandville_mi"
jenison_url = "https://www.manta.com/mb_51_ALL_9O9/jenison_mi"
byron_center_url = "https://www.manta.com/mb_51_ALL_9FI/byron_center_mi"
allendale_url = "https://www.manta.com/mb_51_ALL_9CJ/allendale_mi"
wyoming_url = "https://www.manta.com/mb_51_ALL_WAO/wyoming_mi"
jamestown_url = "https://www.manta.com/mb_51_ALL_9O6/jamestown_mi"
west_olive_url = "https://www.manta.co34rthm/mb_51_ALL_A0O/west_olive_mi"


hudsonville_urls = url_extractor(hudsonville_url)
zeeland_urls = url_extractor(zeeland_url)
grandville_urls = url_extractor(grandville_url)
jenison_urls = url_extractor(jenison_url)
byron_center_urls = url_extractor(byron_center_url)
allendale_urls = url_extractor(allendale_url)
wyoming_urls = url_extractor(wyoming_url)
jamestown_urls = url_extractor(jamestown_url)
west_olive_urls = url_extractor(west_olive_url)


hud_urls = list(flatten(hudsonville_urls))
hud_urls = list(set(hud_urls))

zee_urls = list(flatten(zeeland_urls))
zee_urls = list(set(zee_urls))

grand_urls = list(flatten(grandville_urls))
grand_urls = list(set(grand_urls))

wy_urls = list(flatten(wyoming_urls))
wy_urls = list(set(wy_urls))

jen_urls = list(flatten(jenison_urls))
jen_urls = list(set(jen_urls))

byron_urls = list(flatten(byron_center_urls))
byron_urls = list(set(byron_urls))

allen_urls = list(flatten(allendale_urls))
allen_urls = list(set(allen_urls))

james_urls = list(flatten(jamestown_urls))
james_urls = list(set(james_urls))

west_urls = list(flatten(west_olive_urls))
west_urls = list(set(west_urls))

## Don't forget to do a duplicate check before delivery
manta_scraper(hud_urls, 1966) 
manta_scraper(zee_urls, 1930) 
manta_scraper(grand_urls, 1351) 
manta_scraper(wy_urls, 2136)
manta_scraper(jen_urls, 0) 
manta_scraper(byron_urls, 0) 
manta_scraper(allen_urls, 498) 
manta_scraper(james_urls, 0) 
manta_scraper(west_urls, 0) 



