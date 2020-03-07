## recipe get path
* recipe
  - utter_recipe
* url
  - action_get_recipe
  - utter_food

## recipe fail path
* url
  - action_get_recipe
* url
  - action_get_recipe
  - utter_food

## no recipe path
* navigate
  - action_navigate_recipe
* url
  - action_get_recipe
  - utter_food

## no ingredients path
* ingredients
  - action_recipe_ingredients
* url
  - action_get_recipe
  - utter_food

## creator path
* creators
  - utter_creators

## hello path
* greet
  - utter_greet

## say goodbye
* goodbye
  - utter_goodbye
