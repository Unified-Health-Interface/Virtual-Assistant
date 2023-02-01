from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllUserDoctorNotes(Action):
    def name(self) -> Text:
        return "action_get_all_user_doctor_notes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        notes = requests.get(f"http://0.0.0.0:8000/doctor-note/{tracker.sender_id}").json()

        response = ""

        for note in notes:
            response += f"{note['doctor']} says {note['note']}.\n"

        dispatcher.utter_message(text=response)

        return []
