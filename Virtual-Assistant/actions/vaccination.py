from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllUserVaccinations(Action):
    def name(self) -> Text:
        return "create_get_all_user_vaccinations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        vaccinations = requests.get(f"http://0.0.0.0:8000/vaccination/{tracker.sender_id}").json()

        response = "Your vaccination schedules are:\n"

        for vaccination in vaccinations:
            response += f"{vaccination['id']} - {vaccination['vaccine']} scheduled at on {vaccination['date_time'].split('T')[0]} at {vaccination['date_time'].split('T')[1]}.\n"

        dispatcher.utter_message(text=response)

        return []
