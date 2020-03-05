import re
import random
import requests

import unicodedata
from bs4 import BeautifulSoup

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = (unicodedata.normalize('NFD', text)
            .encode('ascii', 'ignore')
            .decode("utf-8"))

    return str(text)

def fetch_recipe(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser').body

    name = soup.find('h1', id='recipe-main-content').text
    recipe = (soup.find('section', class_='ar_recipe_index'))

    ingredients = scrape_ingredients(recipe)
    directions = scrape_directions(recipe)

    return name, ingredients, directions

def scrape_ingredients(recipe):
    ing_lists = recipe.find_all('ul', id=re.compile(r'lst_ingredients.*'))
    
    for sub_list in ing_lists:
        ingredients += [i.lower() for i in [verify_ingredients(i) for i in sub_list] if i]

    return ingredients

def verify_ingredients(ingredient):
    label = ingredient.find('label')

    if label != -1:
        ng_class = label.attrs.get('ng-class')
        if ng_class and 'false' in label.attrs.get('ng-class'):
            return None
        return label.attrs.get('title')

    return None

def scrape_directions(recipe):
    dir_list = recipe.find('ol', class_='recipe-directions__list').find_all('li')
    return [d.span.text.strip() for d in dir_list]

def main():
    pass

if __name__ == "__main__":
    main()
