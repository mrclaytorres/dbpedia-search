from bs4 import BeautifulSoup
import requests
import random
import pandas as pd
import datetime
import sys
import os
import os.path
import time
import csv
import json
import xmltodict

# Convert rows into ascii
def convert_row( row ):
  row_dict = {}
  for key, value in row.items():
    keyAscii = key.encode('ascii', 'ignore' ).decode()
    valueAscii = value.encode('ascii','ignore').decode()
    row_dict[ keyAscii ] = valueAscii
  return row_dict

def lookup():
    
    time_start = datetime.datetime.now().replace(microsecond=0)
    directory = os.path.dirname(os.path.realpath(__file__))
    
    urls = []
    label = []
    used_query = []
    
    with open('search_query.csv', encoding='unicode_escape') as f:
      reader = csv.DictReader(f)

      for line in reader:

        converted_row = convert_row( line )

        query = converted_row['query']

        print(f'Searching for query: {query}')

        r = requests.get(f'https://lookup.dbpedia.org/api/search?query={query}')
        
        try:
          if r:

            data_dict = xmltodict.parse(r.text)
            results_array = data_dict['ArrayOfResults']['Result']

            for result in results_array:
              used_query.append(query)
              
              label_result = result["Label"] if result["Label"] != '' else "None"
              label.append(label_result)

              uri_result = result["URI"] if result["URI"] != '' else "None"
              urls.append(uri_result)

          else:
            used_query.append(query)
            label.append('None')
            urls.append('None')
            pass

        except:
          used_query.append(query)
          label.append('None')
          urls.append('None')
          pass

    # Save scraped URLs to a CSV file
    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    print('Saving to a CSV file...')
    data = {"Query":used_query, "Label":label, "URI":urls}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()

    filename = f"dbpedialookup{ now }.csv"
    file_path = os.path.join(directory,'csvfiles/', filename)
    df.to_csv(file_path)

    print('Your files are ready.\n')

    time_end = datetime.datetime.now().replace(microsecond=0)
    runtime = time_end - time_start
    print(f"Script runtime: {runtime}.")


if __name__ == '__main__':
    lookup()