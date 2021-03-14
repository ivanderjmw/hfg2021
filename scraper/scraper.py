# -*- coding: utf-8 -*-
from googlemaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import csv
from termcolor import colored
import time


HEADER = ['name', 'details', 'rating', 'address', 'contact']
GOOGLEMAPS_URL_PRE = "https://www.google.com/maps/search/"


def csv_writer(search_query, path='data/'):
    outfile = search_query.strip().replace(" ", "_") + '_gm_results.csv'
    targetfile = open(path + outfile, mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)

    h = HEADER
    writer.writerow(h)

    return writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=100, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='queries.txt', help='search Queries file')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()


    with GoogleMapsScraper(debug=args.debug) as scraper:
        with open(args.i, 'r') as queries_file:
            for query in queries_file:
                url = GOOGLEMAPS_URL_PRE + query.replace(" ", "+")
                n = 0

                # store reviews in CSV file
                writer = csv_writer(query)

                scraper.get_search_page(url)
                    
                while n < args.N:
                    print(colored('[Result ' + str(n) + ']', 'cyan'))
                    results = scraper.get_results_data(0)

                    for r in results:
                        row_data = list(r.values())

                        writer.writerow(row_data)

                    n += len(results)
                    if scraper.more_results() == -1:
                        break