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
        allergies = requests.get(f"http://0.0.0.0:8000/allergy/{tracker.sender_id}").json()

        response = "You are allergic to:\n"

        for allergy in allergies:
            response += f"{allergy['id']} - {allergy['allergy']}\n"

        dispatcher.utter_message(text=response)

        return []


class ActionCheckIfUserHasGivenAllergy(Action):
    def name(self) -> Text:
        return "action_check_if_user_has_given_allergy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        allergies = requests.get(f"http://0.0.0.0:8000/allergy/{tracker.sender_id}").json()

        allergy = next(tracker.get_latest_entity_values("allergy"), None)

        if allergy in [i['allergy'] for i in allergies]:
            response = f"Yes, you are allergic to {allergy}. Take care!"

        else:
            response = f"No, you are not allergic to {allergy}. Stay safe!"

        dispatcher.utter_message(text=response)

        return []
