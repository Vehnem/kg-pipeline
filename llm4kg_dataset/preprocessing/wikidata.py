import json
import xml.etree.ElementTree as ET

tree = ET.parse('/home/marvin/src/llm4kg/data/Q31.json')
root = tree.getroot()

jsonval = json.loads(root.text)

print(jsonval.keys())

print(jsonval['descriptions'])

print(jsonval['sitelinks'].keys())

print(json.dumps(jsonval['claims']['P3212'], indent=4))