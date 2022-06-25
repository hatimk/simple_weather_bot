# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json
import requests


# Informations pour accéder à l'API météo
API_ENDPOINT = 'http://api.weatherapi.com/v1/current.json'
API_KEY = '<CLE_API>'
API_LANG = 'fr'

class ActionTellWeather(Action):

    def name(self) -> Text:
        return "action_tell_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    	# Récupération de nom de ville à partir de la requête
        city = tracker.get_slot('city')

        if city:
        	# Appel GET vers l'API météo
            r = requests.get(API_ENDPOINT + '?'
                             + 'key=' + API_KEY
                             + '&q=' + city
                             + '&lang=' + API_LANG 
            )

            api_resp = json.loads(r.text)

            image = None
            if 'error' in api_resp:
                if api_resp['error']['code'] == 1006:
                    response = 'Désolé, je ne connais aucune ville appelée ' + city + ' :('
                else:
                    response = 'Désolé, je rencontre une difficulté technique pour satisfaire votre requête. Nos équipes se chargent d\'investiguer le problème!'
            else:
            	# Si tout se passe bien, récupération des conditions météo et de l'icone associée
                weather_status = api_resp['current']['condition']['text'].lower()
                response = 'La météo à ' + city + ' affiche un temps ' + weather_status
                image = api_resp['current']['condition']['icon']
        else:
            response = 'Vous souhaitez connaître la météo pour quelle ville? Dites par exemple "Météo Paris"!'

        dispatcher.utter_message(text=response)
        if image:
            dispatcher.utter_message(image=image)

        return []
