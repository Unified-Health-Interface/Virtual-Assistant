from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllUserAllergies(Action):
    def name(self) -> Text:
        return "action_get_all_user_allergies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="Hello, World!")

        allergies = requests.get("http://0.0.0.0:8000/allergy/hari").json()

        response = "You are allergic to:\n"

        for allergy in allergies:
            response += f"{allergy['id']} - {allergy['allergy']}\n"

        dispatcher.utter_message(text=response)

        return []
