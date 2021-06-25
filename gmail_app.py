from __future__ import print_function
import os.path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_email_list():
    service=get_gmail_service()
    results=service.users().messages().list(userId='me',maxResults=5).execute()
    return results.get('messages',[])

def get_email_content(message_id):
    service=get_gmail_service()
    data=service.users().messages().get(userId='me',id=message_id).execute()
    return data


if __name__ == '__main__':
    #messages=get_email_list()
    #for message in messages:
    #    print(message['id'])

    pprint.pprint(get_email_content('17a3e5114762c774'))
    