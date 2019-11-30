from manta import *

hudsonville_url = "https://www.manta.com/mb_51_ALL_9NN/hudsonville_mi"

manta_urls = Manta(city_url=hudsonville_url)
hudsonville_urls = manta_urls.url_extractor()

hud_urls = list(flatten(hudsonville_urls))
hud_urls = list(set(hud_urls))


rows = []
rows.append(['category',"sub_category","sub_sub_category","listing_type","logo","profile_photo","first_name",
             "last_name","email","company","phone_number","fax_number","address1","address2",
             "city","zip_code","state_code","country_code","website","twitter","facebook","linkedin",
             "blog","quote","experience","credentials","awards","youtube","hours","instagram",
             "payments","about_me","password","position","profession_id","services","pinterest",
             "keywords","search_description","additional_phone","additional_email","additional_websites",
             "revenue","employees"])

ms = Manta(urls=hud_urls, site_num=0)
ms.manta_scraper() 

