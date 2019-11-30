from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

import time, re, math, csv, json
from bs4 import BeautifulSoup as soup  # HTML data structure

from tqdm import tqdm

from pandas.core.common import flatten

import proxy_manager as pm
import shadow_useragent, demjson 

def manta_scraper(urls, site_num):
    
    try:
        driver.close()
    except:
        pass
    finally:
        driver = webdriver.Chrome("C:\\Users\\Administrator\\chromedriver.exe")
    
    #if site_num == 0:
    #    rows = []
     #   rows.append(['category',"sub_category","sub_sub_category","listing_type","logo","profile_photo","first_name",
     #   "last_name","email","company","phone_number","fax_number","address1","address2",
     #   "city","zip_code","state_code","country_code","website","twitter","facebook","linkedin",
     #   "blog","quote","experience","credentials","awards","youtube","hours","instagram",
     #   "payments","about_me","password","position","profession_id","services","pinterest",
     #   "keywords","search_description","additional_phone","additional_email","additional_websites",
     #   "revenue","employees"])

        
    count = 1
    for url in tqdm(urls[site_num:], desc="First loop"):
        
        if count % 500 == 0:
            driver.close()
            driver = webdriver.Chrome("C:\\Users\\Administrator\\chromedriver.exe")
        count += 1
        
        try:
            driver.get(url)
        except TimeoutException:
            continue
        pg_source = driver.page_source
        page_soup = soup(pg_source, "html.parser")

        s = page_soup.findAll("script", {"rel":"gtm-data"})[0].text.strip()
        val = "{" + s.split('{', 1)[1].split('visitor_id')[0].strip()
        val = re.sub("\,$",'}', val)
        js = demjson.decode(val)
        
        js1 = json.loads(page_soup.findAll("script", {"type":"application/ld+json"})[0].text.strip())
        
        js2 = json.loads(page_soup.findAll("script", {"type":"application/ld+json"})[1].text.strip())

        elems = page_soup.select("#company-breadcrumbs li span")                      
        try:
            category = js["sic2_desc"]
        except KeyError:
            try:
                category = elems[2].text
            except IndexError:
                category = ""
        
        try:
            sub_category = js["sic4_desc"]
        except KeyError:
            try:
                sub_category = elems[3].text
            except KeyError:
                sub_category = ""
        
        try:
            sub_sub_category = js["sicm_desc"]
        except KeyError:
            try:
                sub_sub_category = elems[4].text
            except IndexError:
                sub_sub_category = ""
            
        try:
            listing_type = js1["@type"]
        except KeyError:
            try:
                listing_type = "Company"
            except:
                listing_type = ""
            
        try:
            logo = js1['logo']
        except KeyError:
            logo = ""
            
        try:
            driver.find_element_by_css_selector(".w30 .text-muted").click()
        except:
            try:
                driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_DOWN)
                driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_DOWN)
                driver.find_element_by_css_selector(".w30 .text-muted").click()
                page_soup = soup(driver.page_source, "html.parser")
                profile_photo = "https:" + page_soup.select(".col-xs-12 img")[0].attrs["src"]
            except:
                profile_photo = ""

        page_soup = soup(pg_source, "html.parser")
        
        try:
            first_name = js1['employee']['givenName']
        except:
            try:
                first_name = js1['employee'][0]['givenName']
            except KeyError:
                first_name = ""
        
        try:
            last_name = js1['employee']['familyName']
        except:
             try:
                 last_name = js1['employee'][0]['familyName']
             except KeyError:
                 last_name = ""
        
        try:
            email = js1['email']
        except KeyError:
            email = ""

        company = js1['name']

        
        try:
            phone_number = js1['telephone']
            phone_number = "-".join(re.findall(r'\d+', phone_number))
        except KeyError:
            phone_number = ""
        
        try:                             
            fax_number = page_soup.select(".text-gray-dark~ div+ div")[0].text.lower()
        except IndexError:
            fax_number = ""
            
        if "fax" not in fax_number:
            fax_number = ""
        else:
            fax_number = re.sub("fax \\| ", "", fax_number)
        
        try:
            address1 = js1['address']['streetAddress']
        except KeyError:
            address1 = ""
        try:
            address2 = js1['address']['addressLocality'] + ", MI " + js1['address']['postalCode']
        except KeyError:
            address2 = ""
        
        try:
            city = js1['address']['addressLocality']
        except KeyError:
            city = ""
            
        try:
            zip_code = js1['address']['postalCode']
        except KeyError:
            zip_code = ""
            
        state_code = "MI"
        country_code = "US"
        
        try:
            website = "https://" + page_soup.select(".break-word a")[0].text.strip()
        except IndexError:
            website = ""
        
        
        def social_selector(media):
            try:
                profile = js1['sameAs']
            except KeyError:
                profile = ""
            
            try:
                sm = profile[[i for i, s in enumerate(profile) if media in s][0]]
            except IndexError:
                sm = ""
            return sm
        
        
        facebook = social_selector("facebook")
        
        twitter = social_selector("twitter")
        
        linkedin = social_selector("linked")
        
        blog = ""
        quote = ""
        try:
            experience = js1['foundingDate']
        except KeyError:
            experience = ""
        
        credentials = page_soup.findAll("li", {"rel":"companyMemberships"})
        credentials = ",\n".join([i.text for i in credentials])
        
        awards = ""
        
        youtube = social_selector("youtube")
        
        try:
            hours = []
            open_hrs_js = js1['openingHoursSpecification']
            for day in open_hrs_js:
                if day['opens'] == "CLOSED":
                    hours.append(day['dayOfWeek'] + " " + day['opens'])
                else:
                    hours.append(day['dayOfWeek'] + " " + day['opens'] + " - " + day['closes'])
            hours = "\n".join(hours)
        except KeyError:
            try:
                hours = page_soup.findAll("div", {"rel":"businessHours"})[0].text.strip()
            except IndexError:
                hours = ""

        instagram = social_selector("instagram")
        
        payments = ""

        try:
            about_me = js1["description"]
        except KeyError:
            about_me = ""
        
        password = ""
        
        try:
            position = js1["employee"]["jobTitle"]
        except:
            try:
                position = js1["employee"][0]["jobTitle"]
            except KeyError:
                position = ""
        
        profession_id = js["sic2_desc"]
        
        try:
            services = js["products"]
        except KeyError:
            services = ""
        
        pinterest = social_selector("pinterest")
        
        keywords = page_soup.find("meta",  property="bt:keywords")["content"]
        
        try:
            search_description = page_soup.findAll("div", {"rel":"about"})[0].text.strip().split('\n')[0]
        except IndexError:
            search_description = ""
            
        try:
            additional_phone = page_soup.select(".border-white+ .col-md-6 .text-gray-dark+ div")[0].text
        except IndexError:
            additional_phone = ""
            
        try:
            additional_email = page_soup.select(".col-md-6:nth-child(3) .text-gray-dark+ div")[0].text
        except IndexError:
            additional_email = ""
        
        try:
            additional_websites = "https://" + page_soup.select("#contact .mtl a")[0].text.strip()
        except IndexError:
            additional_websites = ""
            
        try:
            revenue = page_soup.findAll("td", {"rel":"annualRevenue"})[0].text
        except IndexError:
            revenue = ""
        
        try:
            employees = js1['numberOfEmployees']
        except KeyError:
            try:
                employees = page_soup.findAll("td", {"rel":"numEmployees"})[0].text
            except IndexError:
                employees = ""
    
        
        rr = [category,sub_category,sub_sub_category,listing_type,logo,profile_photo,first_name,
        last_name,email,company,phone_number,fax_number,address1,address2,
        city,zip_code,state_code,country_code,website,twitter,facebook,linkedin,
        blog,quote,experience,credentials,awards,youtube,hours,instagram,
        payments,about_me,password,position,profession_id,services,pinterest,
        keywords,search_description,additional_phone,additional_email,additional_websites,
        revenue,employees]
        
        try:
            rr = [s.encode('ascii', 'ignore').decode("utf-8") for s in rr]
        except AttributeError:
            pass
        
        rows.append(rr)
            
        with open('grandville.csv','w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(rows)
    
        time.sleep(5)






