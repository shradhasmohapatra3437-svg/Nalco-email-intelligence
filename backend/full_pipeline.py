from gmail_fetch import fetch_emails
from pipeline import process_email
from database import init_db, save_email

# Initialize database
init_db()

# Fetch and process emails
emails = fetch_emails(max_results=50, days=30)

for email in emails:
    result = process_email(email['subject'], email['body'])
    
    save_email(
        gmail_id=email['gmail_id'],
        sender=email['sender'],
        subject=email['subject'],
        body=email['body'],
        category=result['category'],
        urgency=result['urgency'],
        summary=result['summary']
    )
    