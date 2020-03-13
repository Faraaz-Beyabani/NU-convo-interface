# Rasa Cooking Assistant Conversational Interface

Group Members: Faraaz Beyabani, Varun Ganglani, Raymond Liu, Brandon Lieuw

On Windows, run `win_setup.ps1` with Powershell to set up the proper virtual environment.
The script will install virtualenv, create a virtual environment, and download all of the necessary packages from the requirements.txt file.

If not on Windows, please create and activate a virtual environment (typically through virtualenv or conda), then install all necessary prerequisites like so: 

`pip install -r requirements.txt`

In order to correctly run the robot on your local machine, please run these two commands in separate terminals in the ChefBot directory:

`rasa run actions`

`rasa shell`

This will allow you to interact with the bot in the terminal in which `rasa shell` was run.

The bot is able to take in recipes, recite ingredients, recite steps one at a time, navigate steps locally (next, previous) or absolutely (1st, 2nd, 3rd). It can also give assistance by linking to Google or YouTube when asked "what is" and "how to" questions, respectively.

Repository: https://github.com/Faraaz-Beyabani/NU-convo-interface/
