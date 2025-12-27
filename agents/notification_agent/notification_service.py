"""
Automatic Notification Service - Fully Fixed
Runs continuously and sends notifications based on schedule
"""
import time
import schedule
from datetime import datetime
from scheduler import NotificationScheduler
from invoice_monitor import InvoiceMonitor
from notification_dispatcher import NotificationDispatcher
from state_manager import StateManager

print("🚀 Starting Notification Service...\n")

# Initialize modules
scheduler = NotificationScheduler()
invoice_monitor = InvoiceMonitor("invoices.json")
dispatcher = NotificationDispatcher(enable_desktop=True)
state_manager = StateManager()

# Show status
print("✅ Modules initialized:")
print("   📊 Scheduler: Enhanced (with time support)")
print("   👁️  Invoice Monitor: Enhanced (datetime aware)")
print("   📤 Dispatcher: Desktop notifications enabled")
print("   📝 State Manager: Ready")
print()

def check_and_notify():
    """Check invoices and send notifications if needed"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking invoices...")

    # Get all invoices needing notification
    invoices = invoice_monitor.get_invoices_needing_notification()

    if not invoices:
        print("  ℹ️  No active invoices found\n")
        return

    print(f"  📋 Found {len(invoices)} active invoice(s):")
    for inv in invoices:
        print(f"     • {inv['invoice_id']}: {inv.get('human_description', 'checking...')}")
    print()

    notifications_sent = 0

    for inv in invoices:
        invoice_id = inv["invoice_id"]
        days_left = inv["days_left"]
        hours_left = inv.get("hours_left", 0)
        time_desc = inv.get("human_description", f"{days_left} days left")

        # Get schedule info
        schedule_info = scheduler.get_schedule_info(days_left, hours_left, time_desc)
        urgency_level = schedule_info["urgency_level"]

        # Check if we should notify now (FIXED METHOD NAME!)
        last_notif_time = state_manager.get_last_notification_time(invoice_id)

        # Get invoice creation time
        invoice_datetime_str = inv.get("invoice_datetime")
        if not invoice_datetime_str:
            invoice_datetime_str = datetime.now().isoformat()

        invoice_dt = datetime.fromisoformat(invoice_datetime_str)

        should_notify = scheduler.should_notify_now(
            last_notif_time,
            urgency_level,
            invoice_dt
        )

        if should_notify:
            # Create message
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
            message = f"{prefix} Invoice #{invoice_id} - {inv['client_name']}: {time_desc}"

            # Send notification
            print(f"  📤 Sending: {message[:70]}...")
            channels = dispatcher.send_notification(
                message=message,
                urgency_level=urgency_level,
                invoice_data=inv
            )

            if channels:
                state_manager.update_notification_sent(invoice_id, channels, urgency_level)
                notifications_sent += 1
                print(f"  ✅ Sent successfully!")
            else:
                print(f"  ⚠️  No channels available")

    if notifications_sent > 0:
        print(f"\n✅ Sent {notifications_sent} notification(s)")
    else:
        print("  ℹ️  No notifications needed at this time")

    print("="*70 + "\n")

# Schedule checks every 15 minutes
schedule.every(15).minutes.do(check_and_notify)

print("✅ Service started!")
print("⏰ Checking invoices every 15 minutes")
print("📋 Press Ctrl+C to stop")
print("="*70 + "\n")

# Run immediately on start
check_and_notify()

# Keep running
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    print("\n\n⚠️  Service stopped by user")
    print("👋 Goodbye!")