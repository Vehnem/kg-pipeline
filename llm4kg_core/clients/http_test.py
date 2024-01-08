import requests
import csv
import jsonlines

plain_rdf=["text/turtle","application/rdf+xml","application/n-triples","application/n-quads","application/trig","application/ld+json"]
data=[]

def rapper_get(url):
    res = requests.get(url,headers={
        'Accept': 'application/n-triples;q=1,'+
        'text/turtle;q=0.9,'+
        'application/n-quads;q=0.9,'+
        'application/ld+json;q=0.8,'+
        'application/rdf+xml;q=0.7,'+
        'application/trig;q=0.7,'+
        '*/*;q=0.5'},allow_redirects=True)
    
    content_type = res.headers['Content-Type'].split(";")[0]
    if content_type in plain_rdf:
        data.append({'url': url, 'type': content_type, 'data': res.text })

# rapper_get("http://dbpedia.org/resource/Albert_Einstein")


# Specify the file path
file_path = "/home/marvin/src/kg-pipeline/examples/formatter_url.csv"

# Open the CSV file
with open(file_path, "r") as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file, delimiter="\t")

    next(csv_reader, None)  # None is to prevent an error if the file is empty

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Process the row data
        uri = row[1].replace("$1", row[2])
        print(uri)
        try:
            rapper_get(uri)
        except:
            
            print("Error")

# Specify the output file path
output_file_path = "/home/marvin/src/kg-pipeline/examples/output.jsonl"

# Write the data array as a JSON Lines file
with jsonlines.open(output_file_path, mode='w') as writer:
    for item in data:
        writer.write(item)
