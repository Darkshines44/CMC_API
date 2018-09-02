#!/usr/bin/env python

import requests
import json
from colorama import Fore, Style
import math


# Given any number (up to 999 trillion) will return 3 digit number with relevant number classification.
def millify(n):
    millnames = ['',' Thousand',' Million',' Billion',' Trillion']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.1f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


# Returns price to cents unless it rounds to 0 cents, then print to 1 s.f.
def round_price(m):
    if '{0:.2f}'.format(m) == '0.00':
        return ( '%s' % float('%.1g' % m) )
    else:
        return ( '{0:.2f}'.format(m) )

def main():

    while True:
        # base URLs
        globalURL = "https://api.coinmarketcap.com/v2/global/"
        tickerURL = "https://api.coinmarketcap.com/v2/ticker/"
        listingURL = "https://api.coinmarketcap.com/v2/listings/"

        # get data from globalURL
        request = requests.get(globalURL)
        data = request.json()
        globalMarketCap = data['data']['quotes']['USD']['total_market_cap']
        
        
        # get data from listings URL
        listing = requests.get(listingURL)
        listing_temp = listing.json()
        listing_data = listing_temp["data"]

        # menu
        print()
        print("Welcome to the CoinMarketCap Explorer!" + '\n')
        print("Global cap of all cryptocurrencies: $" + str(millify(globalMarketCap)) + '\n')
        print("Enter 'all' or the symbol of a crypto asset (i.e. BTC, ETH) to see the name of the top 100 currencies or a specific currency" + '\n')
        choice = input("Your choice: ")


        if choice == "all":
            request = requests.get(tickerURL)
            data = request.json()
            count = 0

            print ('Rank\tSymbol\t\tPrice\t\t\t 1h\t\t24h\t\t7d')

            for x in data['data']:
                count +=1
                ticker = data['data'][str(x)]['symbol']
                price = data['data'][str(x)]['quotes']['USD']['price']
                perc_change = [
                        data['data'][str(x)]['quotes']['USD']['percent_change_1h'],
                        data['data'][str(x)]['quotes']['USD']['percent_change_24h'],
                        data['data'][str(x)]['quotes']['USD']['percent_change_7d']
                        ]
                #Temporary lists to store colours & spacing for price movements
                col_list = []
                spacing_list = []
                
                for item in perc_change:
                    if item == None:
                        col_list.append(Fore.YELLOW)
                        spacing_list.append(' ')
                    elif item < 0:
                        col_list.append(Fore.RED)
                        spacing_list.append('')
                    else:
                        col_list.append(Fore.GREEN)
                        spacing_list.append(' ')

                # Adds spacing to allow for cryptos with over 7 characters in the price string 
                if len('{0:.2f}'.format(price)) < 7:
                    spacing = '\t'
                else:
                    spacing = ''

                # Prints results
                print(str(count) + '\t' + ticker + "\t\t$" + round_price(price), end='')
                print('\t\t' + spacing +  col_list[0] +  spacing_list[0] + str(perc_change[0]) + '%' + Style.RESET_ALL, end='')
                print('\t\t' +  col_list[1] +  spacing_list[1] + str(perc_change[1]) + '%' + Style.RESET_ALL, end='')
                print('\t\t' +  col_list[2] +  spacing_list[2] + str(perc_change[2]) + '%' + Style.RESET_ALL)
            
            print()

        else:
            try:
                LD = next(item for item in listing_data if item["symbol"] == choice)
                Coin_ID = str(LD['id'])
                tickerURL += Coin_ID+'/'
                request = requests.get(tickerURL)
                data = request.json()

                ticker = data['data']['name']
                price = data['data']['quotes']['USD']['price']
                rank = data['data']['rank']
                perc_change = [
                        data['data']['quotes']['USD']['percent_change_1h'],
                        data['data']['quotes']['USD']['percent_change_24h'],
                        data['data']['quotes']['USD']['percent_change_7d']
                        ]

                col_list = []
                
                for item in perc_change:
                    if item == None:
                        col_list.append(Fore.YELLOW)
                    elif item < 0:
                        col_list.append(Fore.RED)
                    else:
                        col_list.append(Fore.GREEN)

                print('\n' + choice + "  " + ticker + " :\t\t$" + round_price(price) +'\n')
                print('Rank:\t' + str(rank) + '\n')
                print('% change 1h:\t\t' + col_list[0] + str(perc_change[0]) + '%' + Style.RESET_ALL)
                print('% change 24h:\t\t' + col_list[1] + str(perc_change[1]) + '%'+ Style.RESET_ALL)
                print('% change 7d:\t\t' + col_list[2] + str(perc_change[2]) + '%' + Style.RESET_ALL)
                print()
                
            except:
                print( Fore.RED + "Asset not Found" + Style.RESET_ALL)

        choice2 = input("Again? (y/n): ")
        if choice2 == "y":
            continue
        if choice2 == "n":
            break

main()
