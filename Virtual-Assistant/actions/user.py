from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetUserDetails(Action):
    def name(self) -> Text:
        return "action_get_user_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        details = requests.get(f"http://0.0.0.0:8000/user/{tracker.sender_id}").json()

        response = f"Your username is {details['username']}.\nYour full name is {details['full_name']}.\nYour user id " \
                   f"is {details['id']}."

        dispatcher.utter_message(text=response)

        return []
