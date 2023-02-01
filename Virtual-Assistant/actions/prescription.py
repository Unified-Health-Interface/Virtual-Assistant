from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllUserPrescriptions(Action):
    def name(self) -> Text:
        return "action_get_all_user_prescriptions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prescriptions = requests.get(f"http://0.0.0.0:8000/prescription/{tracker.sender_id}").json()

        response = ""

        for prescription in prescriptions:
            response += f"{prescription['doctor']} issued a prescription on {prescription['date_time'].split('T')[0]} to take {prescription['medicines']} everyday at {prescription['date_time'].split('T')[1]}.\n"

        dispatcher.utter_message(text=response)

        return []
