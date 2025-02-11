"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com
"""

"""
The formatter module focuses on processing raw text and returning it in 
the required format. 
"""

from datetime import datetime
import math

def formatResult(website, titles, prices, links,ratings,df_flag, currency):
    """
    The formatResult function takes the scraped HTML as input, and extracts the 
    necessary values from the HTML code. Ex. extracting a price '$19.99' from
    a paragraph tag.
    Parameters: titles- scraped titles of the products, prices- scraped prices of the products, 
    links- scraped links of the products on the respective e-commerce sites, 
    ratings-scraped ratings of the product
    Returns: A dictionary of all the parameters stated above for the product
    """

    title, price, link, rating, converted_cur = '', '', '', '', ''
    if titles: title = titles[0].get_text().strip()
    if prices: price = prices[0].get_text().strip()
    if '$' not in price:
        price='$'+price
    if links: link = links[0]['href']
    if ratings: rating = float(ratings[0].get_text().strip().split()[0])
    #if df_flag==0: title=formatTitle(title)
    #if df_flag==0: link=formatTitle(link)
    if currency: converted_cur = getCurrency(currency, price)
    product = {
        'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "title": title,
        "price": price, 
        "link":f'www.{website}.com{link}', 
        "website": website,
        "rating" : rating,
        "converted price": converted_cur
    }
    
    return product


def sortList(arr, sortBy, reverse):
    """ It sorts the products list based on the flags provided as arguements. Currently, it supports sorting by price.
        Parameters- SortBy- "pr": sorts by price, SortBy- "ra": sorts by rating
        Returns- Sorted list of the products based on the parameter requested by the user
    """
    if sortBy == "pr":
        return sorted(arr, key=lambda x: getNumbers(x["price"]), reverse=reverse)
    # To-do: sort by rating
    elif sortBy == "ra":
        return sorted(arr, key=lambda x: getNumbers(x["rating"]), reverse=reverse)
        pass
    return arr

def formatSearchQuery(query):
    """ It formats the search string into a string that can be sent as a url paramenter.
    """
    return query.replace(" ", "+")

def formatTitle(title):
    """ It formats titles extracted from the scraped HTML code.
    """
    if(len(title) > 40):
        return title[:40] + "..."
    return title


def getNumbers(st):
    """ It extracts float values for the price from a string.
    Ex. it extracts 10.99 from '$10.99' or 'starting at $10.99'
    """
    ans = ''
    for ch in st:
        if (ch >= '0' and ch <= '9') or ch == '.':
            ans += ch
    try:
        ans = float(ans)
    except:
        ans = math.inf
    return ans

def getCurrency(currency, price):
    """
    The getCurrency function converts the prices listed in USD to user specified currency. 
    Currently it supports INR, EURO, AUD, YUAN, YEN, POUND
    """

    converted_cur = 0.0
    if len(price)>1 :
        if currency == "inr":
            converted_cur = 75 * int(price[(price.index("$")+1):price.index(".")].replace(",",""))
        elif currency == "euro":
            converted_cur = 1.16 * int(price[(price.index("$")+1):price.index(".")].replace(",",""))
        elif currency == "aud":
            converted_cur = 1.34 * int(price[(price.index("$")+1):price.index(".")].replace(",",""))
        elif currency == "yuan":
            converted_cur = 6.40 * int(price[(price.index("$")+1):price.index(".")].replace(",",""))
        elif currency == "yen":
            converted_cur = 114.21 * int(price[(price.index("$")+1):price.index(".")].replace(",",""))
        elif currency == "pound":
            converted_cur = 0.74 * int(price[(price.index("$")+1):price.index(".")].replace(",",""))
        converted_cur=currency.upper()+' '+str(converted_cur)
    return converted_cur
