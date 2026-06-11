import os
import pickle
import datetime
import re
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def clean_body(text):
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove CSS media queries and other CSS remnants
    text = re.sub(r'@media[^{]*\{[^}]*\}', '', text)
    # Remove HTML entities
    text = re.sub(r'&#?\w+;', ' ', text)
    # Remove dashes and equals
    text = re.sub(r'-{3,}', '', text)
    text = re.sub(r'={3,}', '', text)
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_emails(max_results=10, days=2):
    service = get_gmail_service()
    after = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y/%m/%d')
    results = service.users().messages().list(userId='me', maxResults=max_results, q=f'after:{after}').execute()
    messages = results.get('messages', [])
    
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        
        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        
        body = ''
        
        # Try to get plain text from parts
        if 'parts' in msg_data['payload']:
            for part in msg_data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        break
            # If no plain text, try HTML parts
            if not body:
                for part in msg_data['payload']['parts']:
                    if part['mimeType'] == 'text/html':
                        data = part['body'].get('data', '')
                        if data:
                            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                            break
        elif 'body' in msg_data['payload']:
            data = msg_data['payload']['body'].get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        body = clean_body(body)
        
        emails.append({
            'gmail_id': msg['id'],
            'subject': subject,
            'sender': sender,
            'body': body[:500]
        })
    
    return emails

