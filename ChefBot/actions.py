# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

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
        ingredients += [i for i in [verify_ingredients(i) for i in sub_list] if i]

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

class ActionRecipeGet(Action):

    def name(self) -> Text:
        return "action_recipe_get"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            name, ingredients, directions = fetch_recipe(tracker.latest_message['text'])
            for i in range(len(directions)):
                directions[i] = directions[i].split('. ')
            directions = [(s+'.').replace('..', '.') for d in directions for s in d if s]
        except:
            dispatcher.utter_message(template='utter_get_fail')

        return [SlotSet("name", name), SlotSet("ingredients", ingredients), 
                SlotSet("directions", directions), SlotSet("curr_step", -1)]

class ActionRecipeNavigate(Action):

    def name(self) -> Text:
        return "action_recipe_navigate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if not tracker.get_slot('name'):
            dispatcher.utter_message(template='utter_fail')
            return

        message = tracker.latest_message['text']
        search = re.search(r'[1-9]+(st|nd|rd|th)', message)
        steps = tracker.get_slot('directions')
        curr_step = tracker.get_slot('curr_step')

        word_cardinals = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10, 'eleventh': 11, 'twelfth': 12, 'thirteenth': 13, 'fourteenth': 14, 'fifteenth': 15, 'sixteenth': 16, 'seventeenth': 17, 'eighteenth': 18, 'nineteenth': 19, 'twentieth': 20}

        if search:
            cardinal = search.group()
            num = cardinal[:-2]
            try:
                dispatcher.utter_message(steps[int(num)-1])
                return [SlotSet("curr_step", int(num)-1)] 
            except:
                dispatcher.utter_message(f"I couldn't find the {cardinal} step. Sorry.")
        elif any(w in message for w in word_cardinals.keys()):
            for w in word_cardinals:
                if w in message:
                    try:
                        curr_step = word_cardinals[w]
                        dispatcher.utter_message(steps[curr_step-1])
                        return [SlotSet("curr_step", curr_step-1)] 
                    except:
                        dispatcher.utter_message(f"I couldn't find the {w} step. Sorry.")
                        return
                    
        elif ' next ' in message or ' after ' in message:
            try:
                curr_step += 1
                if curr_step == len(steps) - 1:
                    dispatcher.utter_message("This is the last step:")
                dispatcher.utter_message(steps[curr_step])
                return [SlotSet("curr_step", curr_step)] 
            except:
                dispatcher.utter_message(f"There are no more steps to this recipe.")
        elif ' previous ' in message or ' before ' in message or (' last ' in message and ' was ' in message):
            if curr_step > 0:
                curr_step -= 1
                if curr_step == 0:
                    dispatcher.utter_message("This is the first step:")
                dispatcher.utter_message(steps[curr_step])
                return [SlotSet("curr_step", curr_step)] 
            else:
                dispatcher.utter_message(f"There are no steps before this step.")
        elif ' last ' in message:
            curr_step = len(steps) - 1
            dispatcher.utter_message("This is the last step:")
            dispatcher.utter_message(steps[curr_step])
            return [SlotSet("curr_step", curr_step)] 

class ActionRecipeIngredients(Action):

    def name(self) -> Text:
        return "action_recipe_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if not tracker.get_slot('name'):
            dispatcher.utter_message(template='utter_fail')
            return

        dispatcher.utter_message("Here are the ingredients:")
        for i in tracker.get_slot('ingredients'):
            dispatcher.utter_message(i)

class ActionRecipeHelp(Action):
    def name(self) -> Text:
        return "action_recipe_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if not tracker.get_slot('name'):
            dispatcher.utter_message(template='utter_fail')
            return

        message = tracker.latest_message['text']

        if ' how ' in message:
            dispatcher.utter_message("I think this might help you:")
            dispatcher.utter_message(f"https://www.youtube.com/results?search_query={message.replace(' ', '+')}")
            dispatcher.utter_message("Let me know when you would like to move on.")
        elif ' what ' in message: 
            dispatcher.utter_message("I think this might help you:")
            dispatcher.utter_message(f"https://www.google.com/search?hl=en&q={message.replace(' ', '+')}")
            dispatcher.utter_message("Let me know when you would like to move on.")