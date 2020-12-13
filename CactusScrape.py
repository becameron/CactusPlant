#!/usr/bin/env python3


from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
from datetime import datetime
import os
import CactusCompare, CactusNotification

print('''
CactusScrape is designed to scrape the website cactusplantfleamarket.com
in 5, 15, or 60 minute intervals.

Do you want to run the CactusScrape?
''')

runProgram = input('(yes/no)\n\n').lower()


def startScraper(runProgram):
    if runProgram =='yes':
        scrapeint = int(input('\nDo you want to scrape the website in 5, 15, or 60 minute intervals? (5,15,60)\n'))
        scrapecycle = int(input('How many cycles do you want to run for?\n'))

        if scrapeint in [1,5, 15, 60] and scrapecycle > 0:
            timeKeeper(runProgram,scrapeint,scrapecycle)

def timeKeeper(runProgram,scrapeint,scrapecycle):
    while runProgram == 'yes':
        for i in range(0,scrapecycle):

            CactusProducts = scrapeWebpage()
            writeJson(CactusProducts)

            #makes the program pause for the set interval
            if i == 0:
                print('\nCactusScrape has run 1 time.\n')
                body = CactusCompare.compare_products()

                ##if it comes back with a dictionary, email
                if type(body) != str:
                    CactusNotification.emailNotification(body)
                print(body)

                 ##skips the sleep time if you're only scraping one time.
                if scrapecycle == 1:
                    print('\nCactusScrape has finished running.\n')
                    continue

                time.sleep(scrapeint*60)
                continue

            elif i == (scrapecycle-1):
                print('\nCactusScrape has run '+str(i+1)+' times.\n')
                body = CactusCompare.compare_products()

                ##if it comes back with a dictionary, email
                if type(body) != str:
                    CactusNotification.emailNotification(body)
                print(body)

                print('\nCactusScrape has finished running.')

            else:
                body = CactusCompare.compare_products()

                ##if it comes back with a dictionary, email
                if type(body) != str:
                    CactusNotification.emailNotification(body)
                print(body)

                print('\nCactusScrape has run '+str(i+1)+' times.')
                time.sleep(scrapeint*60)

        runProgram = input('do you want to continue running CactusScrape? (yes/no)\n\n')

def scrapeWebpage():
    #os.chdir(f'~/CactusPlant')
    url = 'https://cactusplantfleamarket.com/'

    ###FireFox to scrape page
    driver = webdriver.Firefox()
    url = 'https://cactusplantfleamarket.com/'
    driver.get(url)
    time.sleep(2) ##waits for javascript to load
    soupObj = BeautifulSoup(driver.page_source,'html.parser')
    driver.quit()

    ##Collects item names and prices
    ProductList = soupObj.find_all(class_='ProductItem__Title-2')
    ProductPrice = soupObj.find_all(class_='ProductItem__Price-2 Price Text--subdued')

    ##Strips off the tags and leaves only the text component
    ProductList2 = []
    ProductPrice2 = []

    for item in ProductList:
        ProductList2.append(item.get_text().strip())

    for item in ProductPrice:
        ProductPrice2.append(item.get_text().strip())

    ##creates final dictionary of item names and prices to be loaded in a json file
    CactusProducts = {}

    for item in range(len(ProductList2)):
        CactusProducts[ProductList2[item]] = ProductPrice2[item]

    return CactusProducts

def writeJson(CactusProducts):
        ##PART 2: write the CactusProducts into a json file

        #gets today's date
        timeStamp = datetime.now().strftime('%H:%M')
        dateStamp = datetime.now().strftime('%Y-%m-%d')

        #tries to load the json file and will enter data if set up.
        try:
            with open('CactusProducts.json','r') as f:
                CactusDict = json.load(f)

            #Checks to see if the current scrape is the first one of the day
            if dateStamp in CactusDict:
                CactusDict[dateStamp].update({timeStamp:CactusProducts})

            else:
                CactusDict[dateStamp] = {timeStamp:CactusProducts}
        except:
            CactusDict = {}
            CactusDict[dateStamp] = {timeStamp:CactusProducts}

        JCactusProducts = json.dumps(CactusDict)
        file = open('CactusProducts.json','w')
        file.write(JCactusProducts)
        file.close()


startScraper(runProgram)
