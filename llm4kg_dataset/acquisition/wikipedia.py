"""Wikimedia tools"""

import requests

def wikitext(resource: str)->str:
    resp = requests.get(resource.replace('/wiki/','/wiki/Special:Export/'))
    return resp.text


def wikiTextsFromList(resources: list[str])->list[str]:
    return [wikitext(x) for x in resources]


def wikiTextsFromCategory(category: str)->list[str]:
    """Get all wikitexts from a category"""
    resp = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:'+category+'&cmlimit=500&format=json')
    return wikiTextsFromList([x['title'] for x in resp.json()['query']['categorymembers'] if x['ns'] == 0])


def wikiTextsFromCategoryRecursive(category: str)->list[str]:
    """Get all wikitexts from a category and its subcategories"""
    resp = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:'+category+'&cmlimit=500&format=json')
    resources = [x['title'] for x in resp.json()['query']['categorymembers'] if x['ns'] == 0]
    subcategories = [x['title'] for x in resp.json()['query']['categorymembers'] if x['ns'] == 14]
    for subcategory in subcategories:
        resources.extend(wikiTextsFromCategoryRecursive(subcategory.replace('Category:','')))
    return wikiTextsFromList(resources)

