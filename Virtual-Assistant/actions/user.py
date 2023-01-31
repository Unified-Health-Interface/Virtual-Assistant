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
        # dispatcher.utter_message(text="Hello, World!")

        details = requests.get("http://0.0.0.0:8000/user/hari").json()

        username = details['username']
        full_name = details['full_name']
        user_id = details['id']

        response = \
            f"""
Your username is {username}.
Your full name is {full_name}.
Your user id is {user_id}.
"""

        dispatcher.utter_message(text=response)

        return []
