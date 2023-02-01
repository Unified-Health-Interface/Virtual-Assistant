from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllUserBills(Action):
    def name(self) -> Text:
        return "action_get_all_user_bills"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bills = requests.get(f"http://0.0.0.0:8000/bill/{tracker.sender_id}").json()

        response = ""

        for bill in bills:
            response += f"Rupees {bill['amount']} is to be paid at {bill['hospital']} for {bill['service']} due {bill['due_date']}.\n"

        dispatcher.utter_message(text=response)

        return []
