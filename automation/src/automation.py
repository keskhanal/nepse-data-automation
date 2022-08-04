#import libraries
import time
import pandas as pd
import bs4 as BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# BaseURL of sharesansar website.
URL = "https://www.sharesansar.com/"

def automate(scripts):
    # Start the Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Hit the url of sharesansar and wait for 2 seconds.
    driver.get(URL)
    time.sleep(2)

    # Enter name of company in searchbox
    driver.find_element('xpath', "//input[@placeholder = 'Company Name or Symbol']").send_keys(scripts)
    time.sleep(2)

    # Click on Search icon
    driver.find_element('xpath', "//b[text() ='" + scripts.upper() + "']").click()
    time.sleep(2)

    # Driver clicks on Price History tab
    driver.find_element('xpath', "//a[text() = 'Price History']").click()
    time.sleep(2)

    # Driver clicks on show entries tab select 50
    driver.find_element('xpath', "//option[text() = '50']").click()
    time.sleep(2)

    final_df = pd.DataFrame()
    
    # Driver clicks on next tab and waits 2 secs until the pagination ends
    for i in range(0, 60):
        # Fetch the webpage and store in a variable.
        webpage = driver.page_source
        HTMLPage = BeautifulSoup.BeautifulSoup(driver.page_source, 'html.parser')

        Table = HTMLPage.find('table', class_='table table-hover table-striped table-bordered compact dataTable no-footer')

        # List of all the rows is store in a variable 'Rows'.
        Rows = Table.find_all('tr', role="row")

        # Empty list is created to store the data of one pagination
        extracted_data = []

        # Loop to go through each row of table
        for i in range(1, len(Rows)):
            try:
                RowDict = {}
                Values = Rows[i].find_all('td')     #extracted all columns of a row

                if len(Values) == 9:
                    #RowDict["SN"] = Values[0].text.replace(',', '')
                    RowDict["Date"] = Values[1].text.replace(',', '')
                    RowDict["Open"] = Values[2].text.replace(',', '')
                    RowDict["High"] = Values[3].text.replace(',', '')
                    RowDict["Low"] = Values[4].text.replace(',', '')
                    RowDict["Close"] = Values[5].text.replace(',', '')
                    RowDict["% change"] = Values[6].text.replace(',', '')
                    RowDict["Volume"] = Values[7].text.replace(',', '')
                    RowDict["TurnOver"] = Values[8].text.replace(',', '')

                    extracted_data.append(RowDict)
            except:
                print("Row Number: " + str(i))
            finally:
                i = i + 1

        extracted_data = pd.DataFrame(extracted_data)
        
        #concatinate list of extracted data to final_df
        final_df=pd.concat([final_df, extracted_data], ignore_index=True)
        
        # Driver clicks on next tab and sleeps for 2 seconds. 
        driver.find_element('xpath', "//a[text() = 'Next']").click()
        time.sleep(2)
        
        i = i+1

    return final_df