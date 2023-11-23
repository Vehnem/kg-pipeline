"""Generate Wikipedia source entries"""
import sys
import csv
import time
import json
import wptools
from datetime import datetime

# Specify the path to your CSV file
csv_file_path = "/home/marvin/src/llm4kg/data/join_imdb-links_sameas-en_specific-type/xaa"

# Open the CSV file
with open(csv_file_path, "r") as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file,delimiter=" ")

    c = 0

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Process each row as needed
        wikidataId=row[0][1:-1].split("/")[-1]
        imbdbId=row[2][1:-1].split("?")[-1]
        wikipediaId=row[5][1:-1].split("/")[-1]
        # wikipediaId=dbpediaId.replace("dbpedia.org/resource","wikipedia.org/wiki")
        type=row[8][1:-1].split("/")[-1]
        
        print(c,datetime.now(),wikidataId,imbdbId,wikipediaId,type,file=sys.stderr)
        # print(row)
        wp_res = wptools.page(wikipediaId,silent=True).get_parse()
        json_tmp = wp_res.data
        json_tmp['wikidataId'] = wikidataId
        json_tmp['imdbId'] = imbdbId
        print(json.dumps(json_tmp))
        time.sleep(1)
        c += 1
