from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllUserAppointments(Action):
    def name(self) -> Text:
        return "action_get_all_user_appointments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        appointments = requests.get(f"http://0.0.0.0:8000/appointment/{tracker.sender_id}").json()

        response = "Your appointments are:\n"

        for appointment in appointments:
            response += f"{appointment['id']} - You have an appointment with {appointment['doctor']} in {appointment['hospital']} on {appointment['date_time'].split('T')[0]} at {appointment['date_time'].split('T')[1]}.\n"

        dispatcher.utter_message(text=response)

        return []
