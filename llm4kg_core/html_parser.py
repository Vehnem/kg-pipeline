import requests
from rdflib import Graph
from bs4 import BeautifulSoup

def extract_ld_json_scripts(html_content):
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first script tag with type="application/ld+json"
    ld_json_scripts = soup.findAll('script', type='application/ld+json')

    # Extract the content of the script tag
    if ld_json_scripts:
        return ld_json_scripts
    else:
        return None


def extract_rdfa(html_content):
    # Create a graph
    g = Graph()

    # Parse the HTML content as RDFa
    g.parse(data=html_content, format='rdfa')

    # Return the graph
    return g