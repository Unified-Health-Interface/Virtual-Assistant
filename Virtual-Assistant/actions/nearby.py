from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetAllNearbyAmenities(Action):
    def name(self) -> Text:
        return "action_get_all_nearby_amenities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        amenity = next(tracker.get_latest_entity_values("amenity"), None)

        request = requests.get("https://nominatim.openstreetmap.org/search",
                               params={"q": f"{amenity} near the international school bangalore",
                                       "format": "json"}).json()[0]

        response = f"The nearest {amenity} to you is {request['display_name']}\n"

        dispatcher.utter_message(text=response)

        return []
