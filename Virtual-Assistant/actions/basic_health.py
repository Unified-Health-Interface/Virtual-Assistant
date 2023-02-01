from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetUserBasicHealthDetails(Action):
    def name(self) -> Text:
        return "action_get_user_basic_health_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        details = requests.get(f"http://0.0.0.0:8000/basic-health/{tracker.sender_id}").json()

        response = f"Your age is {details['age']}.\nYour date of birth is {details['dob']}.\nYour sex is {details['sex']}.\nYour blood group is {details['blood_group']}."

        dispatcher.utter_message(text=response)

        return []
