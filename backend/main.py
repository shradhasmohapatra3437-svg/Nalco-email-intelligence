from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from pipeline import process_email
from database import init_db, save_email, get_all_emails
from gmail_fetch import fetch_emails
from auth import authenticate_user, create_token, get_current_user
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="NALCO Email Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

def fetch_and_classify():
    logging.info("Auto-fetching new emails...")
    emails = fetch_emails(max_results=20, days=2)
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
    logging.info("Auto-fetch complete.")

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_classify, 'interval', minutes=30)
scheduler.start()

class EmailRequest(BaseModel):
    subject: str
    body: str

@app.get("/")
def root():
    return {"status": "NALCO Email Intelligence System is running"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}

@app.post("/process")
def process(email: EmailRequest, current_user=Depends(get_current_user)):
    result = process_email(email.subject, email.body)
    return result

@app.get("/emails")
def get_emails(current_user=Depends(get_current_user)):
    rows = get_all_emails()
    emails = []
    for row in rows:
        emails.append({
            "id": row[0],
            "gmail_id": row[1],
            "sender": row[2],
            "subject": row[3],
            "body_preview": row[4],
            "category": row[5],
            "urgency": row[6],
            "summary": row[7],
            "processed_at": row[8]
        })
    return emails

@app.get("/fetch-now")
def fetch_now(current_user=Depends(get_current_user)):
    fetch_and_classify()
    return {"status": "Fetch complete"}

