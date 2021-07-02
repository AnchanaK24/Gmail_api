from __future__ import print_function
from main import db
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'


def get_gmail_service():
    creds = None
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def mark_as_unread():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    engine.connect()
    rules = json.load(open('rules.json'))
    for rule in rules["1"]["criteria"]:
        print(rule['name'], rule['value'])
        service = get_gmail_service()
        service.users().messages().modify(userId='me', id='17a3e5114762c774',body={'addLabelIds': ['UNREAD']}).execute()
        conn.close

def mark_as_read():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    engine.connect()
    rules = json.load(open('rules.json'))
    for rule in rules["1"]["criteria"]:
        print(rule['name'], rule['value'])
        service = get_gmail_service()
        service.users().messages().modify(userId='me', id='17a3e5114762c774',body={'removeLabelIds': ['UNREAD']}).execute()
        conn.close()

def starred():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    engine.connect()
    rules = json.load(open('rules.json'))
    for rule in rules["1"]["criteria"]:
        print(rule['name'], rule['value'])
        service = get_gmail_service()
        service.users().messages().modify(userId='me', id='17a3e5114762c774', body={'addLabelIds': ['STARRED']}).execute()
        conn.close()

def archive():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    engine.connect()
    rules = json.load(open('rules.json'))
    for rule in rules["1"]["criteria"]:
        print(rule['name'], rule['value'])
        service = get_gmail_service()
        service.users().messages().modify(userId='me', id='17a3e5114762c774', body={'addLabelIds': ['INBOX']}).execute()
        conn.close()

def add_label():
    service = get_gmail_service()
    label={
        "labelListVisibility":"labelShow",
        "messageListVisibility":"show",
        "name":"Delete"
    }
    result=service.users().labels().create(userId='me', body=label).execute()
    print(result)

if __name__ == '__main__':
    mark_as_unread()
    starred()
    archive()
    add_label()
