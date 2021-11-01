"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

import argparse
import scraper
import formatter
from tabulate import tabulate
import pandas as pd
import os
import csv_writer


def main():
    parser = argparse.ArgumentParser(description="Slash")
    parser.add_argument('--open', type=str, help="Open Full Program; T for yes F for mini version", default="F")
    parser.add_argument('--search', type=str, help='Product search query')
    parser.add_argument('--num', type=int, help="Maximum number of records", default=3)
    parser.add_argument('--sort', type=str, nargs='+', help="Sort according to re (relevance: default), pr (price) or ra (rating)", default="re")
    parser.add_argument('--link', action='store_true', help="Show links in the table")
    parser.add_argument('--des', action='store_true', help="Sort in descending (non-increasing) order")
    parser.add_argument('--cd', type=str,  help="Change directory to save CSV file with search results", default=os.getcwd())
    args = parser.parse_args()
    if(args.open=='T'):
        print("open full")
        return
    products_1 = scraper.searchAmazon(args.search)
    products_2 = scraper.searchWalmart(args.search)

    for sortBy in args.sort:
        products1 = formatter.sortList(products_1, sortBy, args.des)[:args.num]
        products2 = formatter.sortList(products_2, sortBy, args.des)[:args.num]
        results = products1 + products2
        results = formatter.sortList(results, sortBy, args.des)


    print()
    print()
    print(tabulate(results, headers="keys", tablefmt="github"))
    print()
    print()
    print("CSV Saved at: ",os.getcwd())
    print("File Name:", csv_writer.write_csv((products_1+products_2), args.search, args.cd))
    
    

if __name__ == '__main__':
    main()