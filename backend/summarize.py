import ollama

def summarize_email(subject, body):
    prompt = f"""You are an email summarizer for NALCO, a government aluminium company.

Summarize the following email in exactly 2-3 actionable lines.
Be concise. Focus on what needs to be done or what the email is about.

Email Subject: {subject}
Email Body: {body}

Reply with only the summary. Nothing else."""

    response = ollama.chat(model="gemma3:1b", messages=[
        {"role": "user", "content": prompt}
    ])

    return response["message"]["content"].strip()

# Test
subject = "My laptop is not connecting to the office WiFi"
body = "Hi team, since yesterday my laptop refuses to connect to the internal network. I have tried restarting but no luck. Please help."

summary = summarize_email(subject, body)
print(f"Summary: {summary}")
