# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import re
import random
import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import unicodedata
from bs4 import BeautifulSoup

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
    ingredients = []
    
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

class ActionGetRecipe(Action):

    def name(self) -> Text:
        return "action_get_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            name, ingredients, directions = fetch_recipe(tracker.latest_message['text'])
        except:
            dispatcher.utter_message(template='utter_fail')

        return [SlotSet("name", name), SlotSet("ingredients", ingredients), 
                SlotSet("directions", directions), SlotSet("curr_step", -1)]

class ActionNavigateRecipe(Action):

    def name(self) -> Text:
        return "action_navigate_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if not tracker.get_slot('name'):
            dispatcher.utter_message(template='utter_fail')
        else:
            pass

class ActionRecipeIngredients(Action):

    def name(self) -> Text:
        return "action_recipe_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if not tracker.get_slot('name'):
            dispatcher.utter_message(template='utter_fail')
        else:
            pass

