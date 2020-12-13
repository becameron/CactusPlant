import json
from pprint import pprint

def get_product_data():
    with open('CactusProducts.json','r') as f:
              CactusDict = json.load(f)

    ##Gets the most recent date
    dates = sorted(CactusDict.keys())
    current_date = max(dates)

    ##Gets the most recent time.
    time_keys = sorted(CactusDict[current_date].keys())
    now_time_key = max(time_keys)

    ##checks if it's the first entry of the day
    entries_today = len(CactusDict[current_date])

    if entries_today == 1:

        ## if it is the first entry of the day, gets the previous date.
        dates.remove(current_date)

        try:
            previous_date = max(dates)
        except:
            print('First time program has been run!/n')
            previous_date = current_date 
        prev_time_key = max(CactusDict[previous_date])

        OldCactusProds = CactusDict[previous_date][prev_time_key]


    else:
        ##if it's not the first entry, get the second most recent time from today.
        time_keys.remove(now_time_key)
        prev_time_key = max(time_keys)

        OldCactusProds = CactusDict[current_date][prev_time_key]

    NewCactusProds = CactusDict[current_date][now_time_key]

    return NewCactusProds,OldCactusProds

def compare_products():
    ##compares the two most recent data scrapes from the website
    NewCactusProds,OldCactusProds = get_product_data()

    ChangeListing = {}

    for product in NewCactusProds:
        if product in OldCactusProds:
            #checks prices of existing products
            if OldCactusProds[product] != NewCactusProds[product]:

                if 'Price Change' in ChangeListing:
                    ChangeListing['Price Change'].update({product:{
                    'New Price':NewCactusProds[product],'Previous Price':OldCactusProds[product]
                    }
                    })
                else:
                    ChangeListing['Price Change'] = {
                    product:{
                    'New Price':NewCactusProds[product],'Previous Price':OldCactusProds[product]
                            }
                    }

        else:
            #if product isn't in previous products, it's new.
            if 'New Product' in ChangeListing:
                    ChangeListing['New Product'].update({product:NewCactusProds[product]
                    })
            else:
                    ChangeListing['New Product'] = {
                    product:NewCactusProds[product]
                    }

    #return ChangeListing
    if len(ChangeListing) == 0:
        return 'No new products. No new products or price changes. None.'
    else:
        return ChangeListing
