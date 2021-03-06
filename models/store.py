from __future__ import print_function
from main import db
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from models.gmail import get_mail

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


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
    engine = db.create_engine('sqlite:///user.db', echo=True)
    conn = engine.connect()
    result = get_mail(''17a3e5114762c774'')
    conn.execute('INSERT INTO mail(mail_from,mail_to,mail_subject,mail_date)  VALUES(:mail_from,:mail_to,:mail_subject,:mail_date)',
                 results['from'], results['to'], results['subject'], results['date'])
    print("entered successfully")
    conn.close()

 
def mark_as_unread():
    rules = json.load(open('rules.json'))
    for rule in rules["rule1"]["fields"]:
        print(rule['name'], rule['value'])
        service = get_gmail_service()
        service.users().messages().modify(userId='me', id=''17a3e5114762c774'',
                                          body={'addLabelIds': ['UNREAD']}).execute()

        
        
 def mark_as_read():
    rules = json.load(open('rules.json'))
    for rule in rules["rule1"]["fields"]:
        print(rule['name'], rule['value'])
        service = get_gmail_service()
        service.users().messages().modify(userId='me', id=''17a3e5114762c774'',
                                          body={'removeLabelIds': ['UNREAD']}).execute()


def archive_mail():
    rules = json.load(open('rules.json'))
    for rule in rules["rule1"]["fields"]:
        print(rule['name'], rule['value'])
        service = get_gmail_service()
        service.users().messages().modify(userId='me', id=''17a3e5114762c774'',
                                          body={'removeLabelIds': ['INBOX']}).execute()


    
    
    if __name__ == '__main__':
    #store()
    #mark_as_unread()
    #mark_as_read()
    #archive_mail()
