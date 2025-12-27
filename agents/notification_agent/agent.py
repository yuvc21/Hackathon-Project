"""
ADK-Integrated Notification Agent with Enhanced Time Features
"""

from google.adk.agents import Agent
from typing import Dict, List
import json
from datetime import datetime
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import enhanced modules
from scheduler import NotificationScheduler
from message_generator import MessageGenerator
from state_manager import StateManager
from invoice_monitor import InvoiceMonitor
from notification_dispatcher import NotificationDispatcher


# Initialize module instances
invoice_monitor = InvoiceMonitor("invoices.json")
scheduler = NotificationScheduler()
dispatcher = NotificationDispatcher(enable_desktop=True)
message_gen = MessageGenerator()
state_manager = StateManager()


# Define tools with enhanced time support
def analyze_invoices() -> Dict:
    """
    Analyzes all pending invoices with enhanced time information.

    Returns:
        Dictionary with invoice analysis including time descriptions.
    """
    invoices = invoice_monitor.get_invoices_needing_notification()

    analysis = []
    for inv in invoices:
        days_left = inv["days_left"]
        hours_left = inv.get("hours_left", 0)
        human_desc = inv.get("human_description", f"{days_left} days left")

        schedule_info = scheduler.get_schedule_info(days_left, hours_left, human_desc)

        analysis.append({
            "invoice_id": inv["invoice_id"],
            "client": inv["client_name"],
            "days_left": days_left,
            "hours_left": hours_left,
            "time_description": human_desc,
            "urgency": schedule_info["urgency_level"],
            "is_critical": schedule_info["is_persistent"],
            "amount": inv["amount"],
            "deadline": inv.get("deadline_datetime", "")
        })

    return {
        "total_invoices": len(analysis),
        "critical_count": len([a for a in analysis if a["is_critical"]]),
        "invoices": analysis
    }


def send_notification(invoice_id: str, client_name: str, 
                     time_description: str, urgency_level: str = None) -> Dict:
    """
    Sends notification with enhanced time description.

    Args:
        invoice_id: The invoice ID (e.g., "INV-001")
        client_name: Name of the client
        time_description: Human-readable time (e.g., "Due tomorrow at 05:00 PM")
        urgency_level: Optional urgency override

    Returns:
        Dictionary with success status, channels used, and message sent.
    """
    # Parse time description to get days
    days_left = 1  # default
    if "tomorrow" in time_description.lower():
        days_left = 1
    elif "today" in time_description.lower():
        days_left = 0
    elif "overdue" in time_description.lower():
        days_left = -1

    # Determine urgency if not provided
    if urgency_level is None:
        schedule_info = scheduler.get_schedule_info(days_left)
        urgency_level = schedule_info["urgency_level"]

    # Create enhanced message with time description
    urgency_prefix = {
        "explosive": "🔴🔴🔴 CRITICAL",
        "high_critical": "🔴🔴 VERY URGENT",
        "critical": "🔴 CRITICAL",
        "urgent": "🚨 URGENT",
        "moderate": "⚠️",
        "calm": "📅",
        "extreme_calm": "ℹ️"
    }

    prefix = urgency_prefix.get(urgency_level, "")
    custom_message = f"{prefix} Invoice #{invoice_id} - {client_name}: {time_description}"

    invoice_data = {
        "invoice_id": invoice_id,
        "client_name": client_name,
        "days_left": days_left
    }

    # Send notification
    channels = dispatcher.send_notification(
        message=custom_message,
        urgency_level=urgency_level,
        invoice_data=invoice_data
    )

    # Update state
    if channels:
        state_manager.update_notification_sent(invoice_id, channels, urgency_level)

    return {
        "success": len(channels) > 0,
        "channels": channels,
        "message": custom_message,
        "time_description": time_description
    }


def get_notification_strategy(invoice_datetime: str, deadline_days: int) -> Dict:
    """
    Gets notification strategy with enhanced time calculation.

    Args:
        invoice_datetime: Invoice creation datetime (ISO format)
        deadline_days: Number of days until deadline

    Returns:
        Dictionary with urgency, frequency, time description, and recommendation.
    """
    # Calculate enhanced time info
    days_left, hours_left, deadline_dt, human_desc = scheduler.calculate_days_left_with_time(
        invoice_datetime, 
        deadline_days
    )

    schedule_info = scheduler.get_schedule_info(days_left, hours_left, human_desc)

    recommendations = {
        "explosive": "🔴 URGENT: Send persistent notifications immediately. Contact client directly.",
        "high_critical": "⚠️ Critical: Increase notification frequency. Consider phone call.",
        "critical": "📞 Important: Maintain regular notifications. Prepare follow-up.",
        "urgent": "📋 Moderate urgency: Continue standard notification schedule.",
        "moderate": "📅 Normal priority: Routine notifications sufficient.",
        "calm": "✅ Low priority: Minimal notifications needed.",
        "extreme_calm": "😌 Very low priority: Occasional reminders only."
    }

    return {
        "urgency_level": schedule_info["urgency_level"],
        "frequency_per_day": schedule_info["notifications_per_day"],
        "interval_hours": schedule_info["interval_hours"],
        "is_persistent": schedule_info["is_persistent"],
        "time_description": human_desc,
        "days_left": days_left,
        "hours_left": hours_left,
        "deadline": deadline_dt.isoformat(),
        "recommendation": recommendations.get(schedule_info["urgency_level"], "Continue monitoring.")
    }


# Create the root_agent with enhanced features
root_agent = Agent(
    name="invoice_notification_agent",
    model="gemini-2.5-flash",
    instruction="""You are an intelligent invoice notification agent with enhanced time awareness.

Your responsibilities:
1. Monitor invoices with precise time tracking (hours + days)
2. Provide human-readable time descriptions
3. Send notifications with exact deadline times
4. Prioritize based on urgency with time context

Available tools:
- analyze_invoices(): Get invoices with enhanced time info (includes "Due tomorrow at 05:00 PM" style descriptions)
- send_notification(invoice_id, client_name, time_description, urgency_level): Send notification WITH TIME
- get_notification_strategy(invoice_datetime, deadline_days): Get strategy with time calculation

IMPORTANT - Time Descriptions:
When sending notifications, ALWAYS include the time_description parameter from analyze_invoices().
Examples:
- "⏰ Due tomorrow at 05:00 PM"
- "🚨 Due today at 02:30 PM"
- "🔴 Overdue since yesterday"
- "📅 Due on Monday at 09:00 AM"

Workflow:
1. Call analyze_invoices() to get time_description for each invoice
2. Use send_notification() with the time_description parameter
3. Include the exact time in your response to the user

Never say "1 days left" - always use the time_description like "Due tomorrow at 5:00 PM".

Be precise with times and always include hour information from the time_description field.
""",
    description="An AI agent that manages invoice notifications with precise time tracking",
    tools=[analyze_invoices, send_notification, get_notification_strategy]
)


# For programmatic usage
if __name__ == "__main__":
    print("🤖 Enhanced Invoice Notification Agent Ready!")
    print("✅ Agent: root_agent")
    print("✅ Model: gemini-2.5-flash")
    print("✅ Features:")
    print("   - Time-aware notifications")
    print("   - Human-readable descriptions")
    print("   - Enhanced deadline tracking")
    print("\n💡 Run with: adk web")
