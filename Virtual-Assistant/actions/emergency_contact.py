import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Text, Dict, List

import requests
from dotenv import load_dotenv
from notify_run import Notify
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from twilio.rest import Client

load_dotenv()


def send_notify_notification(endpoint, message):
    notify = Notify()
    notify.endpoint = endpoint

    notify.send(message)


def send_emails(emails, body):
    context = ssl.create_default_context()

    subject = "IMPORTANT!!!"
    body = body
    sender_email = os.getenv('GMAIL_EMAIL')
    sender_password = os.getenv('GMAIL_PASSWORD')

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(sender_email, sender_password)

        for receiver_email in emails:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message["Bcc"] = receiver_email

            message.attach(MIMEText(body, "plain"))

            server.sendmail(sender_email, receiver_email, message.as_string())


def send_calls(phones, message):
    phone_number = os.getenv('PHONE_NUMBER')
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    for phone in phones:
        call = client.calls.create(twiml=f'<Response><Say>{message}</Say></Response>',
                                   to=phone, from_=phone_number)

        print(call.sid)


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
        response = "Calling all your emergency contacts!"

        dispatcher.utter_message(text=response)

        contacts = requests.get(f"http://0.0.0.0:8000/emergency-contact/{tracker.sender_id}").json()
        full_name = requests.get(f"http://0.0.0.0:8000/user/{tracker.sender_id}").json()['full_name']
        endpoint = requests.get(f"http://0.0.0.0:8000/notify-runner/{tracker.sender_id}").json()['endpoint']

        email_addresses = [contact['email'] for contact in contacts]
        phone_numbers = [contact['phone'] for contact in contacts]

        message = f"{full_name} has rung the alarm! They are in danger! They need help! Please look into it immediately!"

        send_notify_notification(endpoint, message)
        send_emails(email_addresses, message)
        send_calls(phone_numbers, message)

        return []
