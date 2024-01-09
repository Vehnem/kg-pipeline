import json

# Specify the path to the file
file_path = "/home/marvin/src/llm4kg/data/examples/wikipedia/head.json"

# Open the file in read mode
with open(file_path, "r") as file:
    # Read each line in the file
    for line in file:
        # Parse the JSON object
        json_object = json.loads(line)
        print(json_object['wikidata'])
        
        # Process the JSON object as needed
        # ...
