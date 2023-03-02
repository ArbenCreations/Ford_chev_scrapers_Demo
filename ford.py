from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=en')
chrome_options.add_argument("--user-agent=Mozilla/5.0")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--mute-audio")
driver = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())

main_data=[]
vins=pd.read_csv(r'ford vins.csv')
for vin_i in vins['vin']:
    driver.get('https://www.ford.com/support/recalls/')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//h3[@id="vin-label"]')))
    except:
        pass
    try:
        vin=driver.find_element_by_xpath('//input[@id="vin-field-vin-selector-label"]')
        vin.clear()
        vin.send_keys(str(vin_i))
        driver.find_element_by_xpath('//button[@data-testid="vin-submit-button"]').click()
    except:
        pass
    
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="recalls-title"]')))
    except:
        pass
    try:
        driver.find_element_by_id('vin-field-vin-selector-error-message')
        print('Wrong Vin')
    except:
        time.sleep(2)
        status=''
        name=''
        NHTSA=''
        date=''
        description=''
        safetyRisk=''
        remedy=''   
        try:
            st=driver.find_element_by_xpath('//div[@class="recalls-section no-recalls"]')
            st='No'
        except:
            st='yes'
            soup=BeautifulSoup(driver.page_source,'html.parser')

            support_accordion=soup.find('div',attrs={'class':'support-accordion'}).find_all('div',attrs={'class':'accordion-item'})

            for item in support_accordion:
                name=str(item.find('span',attrs={'class':'accordion-title'}).text.strip())
                status=str(item.find('span',attrs={'class':'accordion-subtitle'}).text.replace('Recall','').strip())
                # print(name)
                # data=driver.find_element_by_id(name).find_elements_by_tag_name('div')
                data=soup.find('div',attrs={'id':name}).find_all('div')
                date=data[1].text
                description=data[3].text
                safetyRisk=data[5].text
                remedy=data[7].text
                NHTSA=data[9].text


        item_data={
            # 'Open Recalls':gfas['data']['vin'],
                    'Recall status':status,
                    'Name of Recall':name,
                    'Campaign/NHTSA':NHTSA,
                    'Date of recall':date,
                    'description':description,
                    'Safety Risk':safetyRisk,
                    'Remedy':remedy,
                    'VIN':vin_i,
                    'Open Recalls':st,
        }
        main_data.append(item_data)
        pd.DataFrame(main_data).to_csv('ford.csv',index=False)
driver.quit()


