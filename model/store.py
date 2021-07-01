from __future__ import print_function
from main import db
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from service.gmail_api import get_email_content(message_id)

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


def store():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    conn = engine.connect()
    result= get_email_content('17a3e5114762c774')
    conn.execute('INSERT INTO mail(mail_from,mail_to,mail_subject,mail_date) VALUES (:mail_from,:mail_to,:mail_subject,:mail_date)',
                 result['from'], result['to'], result['subject'], result['date'])
    print('logged successfully')
    conn.close()




if __name__ == '__main__':
    store()