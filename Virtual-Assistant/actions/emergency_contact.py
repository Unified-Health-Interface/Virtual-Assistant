from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from notify_run import Notify


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


class ActionCallAllUserEmergencyContacts(Action):
    def name(self) -> Text:
        return "action_call_all_user_emergency_contacts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        contacts = requests.get(f"http://0.0.0.0:8000/emergency-contact/{tracker.sender_id}").json()
        endpoint = requests.get(f"http://0.0.0.0:8000/notify-runner/{tracker.sender_id}").json()['endpoint']

        email_addresses = [contact['email'] for contact in contacts]
        phone_numbers = [contact['phone'] for contact in contacts]

        notify = Notify()
        notify.endpoint = endpoint

        notify.send(f"{tracker.sender_id} is in danger! {tracker.sender_id} needs help!")

        response = "Calling all your emergency contacts!"

        dispatcher.utter_message(text=response)

        return []
