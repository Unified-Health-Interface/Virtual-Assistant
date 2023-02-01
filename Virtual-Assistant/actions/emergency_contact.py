from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllUserEmergencyContacts(Action):
    def name(self) -> Text:
        return "action_get_all_user_emergency_contacts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        contacts = requests.get(f"http://0.0.0.0:8000/emergency-contact/{tracker.sender_id}").json()

        response = ""

        for contact in contacts:
            response += f"Emergency contact {contact['name']} has email {contact['email']} and phone number {contact['phone']}.\n"

        dispatcher.utter_message(text=response)

        return []
