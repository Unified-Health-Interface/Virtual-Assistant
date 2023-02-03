import os
from typing import Any, Text, Dict, List

from dotenv import load_dotenv
from newsapi import NewsApiClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

load_dotenv()


class ActionGetAllHealthNews(Action):
    def name(self) -> Text:
        return "action_get_all_health_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        newsapi = NewsApiClient(api_key=os.getenv('NEWSAPI_API'))

        response = ".\n".join(
            [i['title'] for i in newsapi.get_top_headlines(category='health', language='en', country='in')['articles']][
            :3])

        dispatcher.utter_message(text=response)

        return []
