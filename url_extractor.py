def url_extractor(city_url):
    driver.get(city_url)
    page_soup = soup(driver.page_source, "html.parser")
    urls = ["https://www.manta.com" + i.attrs["href"] for i in page_soup.select(".mbm a")]
    
    time.sleep(5)
    
    city_urls = []
    for url in tqdm(urls, desc = "First loop"):
        driver.get(url)
        page_soup = soup(driver.page_source, "html.parser")
        try:
            p = page_soup.findAll("p", {"class":"text-primary pl-xs count-line"})[0].text.strip().replace(',','')
        except:
            continue
        total = [int(s) for s in p.split() if s.isdigit()][0]
        num_of_pages = math.ceil(total / 35)
        
        if num_of_pages > 1:
            for page_num in tqdm(range(num_of_pages), desc = "Second loop"):
                time.sleep(5)
                
                if page_num == 0:
                    page_soup = soup(driver.page_source, "html.parser")
                    try:
                       p = [i.attrs["content"] for i in page_soup.findAll("meta", {"itemprop":"url"})]
                    except:
                        
                        return city_urls
                    city_urls.append(p)
                else:
                    driver.get(url + "?pg=" + str(page_num+1))
                    page_soup = soup(driver.page_source, "html.parser")
                    try:
                       p = [i.attrs["content"] for i in page_soup.findAll("meta", {"itemprop":"url"})]
                    except:
                        return city_urls
                    city_urls.append(p)
                    
                
        else:
            page_soup = soup(driver.page_source, "html.parser")
            try:
                p = [i.attrs["content"] for i in page_soup.findAll("meta", {"itemprop":"url"})]
            except:
                return city_urls
            city_urls.append(p)
            
        time.sleep(5)    
            
    return city_urls