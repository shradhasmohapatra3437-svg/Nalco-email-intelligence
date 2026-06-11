from classify import classify_email
from summarize import summarize_email
import ollama

def detect_urgency(subject, body):
    prompt = f"""You are an email urgency detector for NALCO, a government aluminium company.

Classify the urgency of the following email as exactly ONE of:
- High
- Medium
- Low

High = immediate action required, deadlines, incidents, failures
Medium = action needed but not immediately, scheduled tasks, requests
Low = informational, FYI, no action needed

Email Subject: {subject}
Email Body: {body}

Reply with only the urgency level. Nothing else."""

    response = ollama.chat(model="gemma3:1b", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"].strip()

def process_email(subject, body):
    category = classify_email(subject, body)
    summary = summarize_email(subject, body)
    urgency = detect_urgency(subject, body)

    return {
        "subject": subject,
        "category": category,
        "urgency": urgency,
        "summary": summary
    }

# Test with 3 emails
emails = [
    {
        "subject": "My laptop is not connecting to the office WiFi",
        "body": "Hi team, since yesterday my laptop refuses to connect to the internal network. I have tried restarting but no luck. Please help."
    },
    {
        "subject": "Salary slip for May 2026 not received",
        "body": "Dear HR, I have not received my salary slip for the month of May 2026. Kindly look into this and share it at the earliest."
    },
    {
        "subject": "Quarterly safety audit scheduled for next week",
        "body": "All department heads are informed that the quarterly safety audit will be conducted from June 9 to June 11. Please ensure all safety logs are updated."
    }
]

for email in emails:
    result = process_email(email["subject"], email["body"])
    print(f"\nSubject:  {result['subject']}")
    print(f"Category: {result['category']}")
    print(f"Urgency:  {result['urgency']}")
    print(f"Summary:  {result['summary']}")
    print("-" * 60)
    