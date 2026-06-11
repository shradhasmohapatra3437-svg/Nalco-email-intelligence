import ollama

def classify_email(subject, body):
    prompt = f"""You are an email classifier for NALCO, a government aluminium manufacturing company in India.

Classify the email into exactly ONE of these categories:
- Finance: budget, payments, invoices, expenses, reimbursements, salary, payroll
- HR: leaves, recruitment, appraisals, salary slips, employee welfare, training
- Systems/IT: computers, software, network, wifi, server, hardware, IT support
- Procurement: purchase orders, vendors, supplies, contracts, tenders
- Operations: production, plant, machinery, maintenance, schedules
- Legal/Vigilance: legal notices, compliance, vigilance, disputes
- Administration: office management, facilities, stationery, housekeeping
- Safety/Environment: safety audits, accidents, environment, hazards
- Friends/Family: personal emails, greetings, casual messages
- Others: anything that doesn't fit above categories

Examples:
Subject: Salary slip for April not received
Body: I have not received my salary slip for April. Please send it.
Category: HR

Subject: May salary not credited to account
Body: My salary for May has not been credited. Please check with finance.
Category: Finance

Subject: Increment letter and appraisal result
Body: Please share my appraisal result and revised salary structure.
Category: HR

Subject: Invoice payment pending for vendor ABC
Body: The payment for invoice #1234 is overdue. Please process it.
Category: Finance

Subject: WiFi not working in Block B
Body: The internet connection in Block B has been down since morning.
Category: Systems/IT

Subject: Safety drill scheduled for Friday
Body: All employees must attend the fire safety drill on Friday at 10am.
Category: Safety/Environment

Now classify this email:
Subject: {subject}
Body: {body}

Reply with only the category name. Nothing else."""

    response = ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0}
    )
    return response["message"]["content"].strip()

# Test
subject = "Salary slip for May 2026 not received"
body = "Dear HR, I have not received my salary slip for the month of May 2026. Kindly look into this and share it at the earliest."

category = classify_email(subject, body)
print(f"Category: {category}")
