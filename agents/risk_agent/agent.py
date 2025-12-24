from google.adk.agents.llm_agent import Agent
from datetime import datetime


def check_msme_payment_overdue(invoice_id: str, vendor_name: str, amount: float, invoice_date: str) -> dict:
    """Check if MSME payment violates Section 43B(h) 45-day rule"""
    days = (datetime.now() - datetime.strptime(invoice_date, '%Y-%m-%d')).days
    overdue_days = max(0, days - 45)
    
    return {
        "invoice_id": invoice_id,
        "risk_level": "HIGH" if overdue_days > 0 else "LOW",
        "overdue_days": overdue_days,
        "tax_penalty": amount * 0.35 if overdue_days > 0 else 0,
        "whatsapp_alert": f"🚨 Invoice #{invoice_id}\nPay {vendor_name} ₹{amount/1000:.0f}K\n{overdue_days} days OVERDUE!"
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='risk_agent',
    tools=[check_mjsme_payment_overdue],
    description='A helpful assistant for user questions.',
    instruction="""MSME Payment Alert Agent. Indian tax law Section 43B(h): 
    Companies must pay MSMEs within 45 days or lose tax deduction.
    Analyze invoices → Flag overdue → Generate alert notifications."""
)
