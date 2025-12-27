"""
Complete Enhanced Notification Test
Uses enhanced time features + sends real desktop notifications
"""
from datetime import datetime, timedelta
import json
import time

print("🔔 ENHANCED NOTIFICATION TEST WITH DESKTOP POPUPS\n")
print("="*70 + "\n")

# Import enhanced modules + dispatcher
try:
    from scheduler_enhanced import NotificationScheduler
    from invoice_monitor_enhanced import InvoiceMonitor
    from notification_dispatcher import NotificationDispatcher
    from message_generator import MessageGenerator
    from state_manager import StateManager

    print("✅ All modules imported successfully!\n")
    modules_loaded = True
except ImportError as e:
    print(f"❌ Import error: {e}\n")
    print("Make sure these files exist:")
    print("  - scheduler_enhanced.py")
    print("  - invoice_monitor_enhanced.py")
    print("  - notification_dispatcher.py")
    print("  - message_generator.py")
    print("  - state_manager.py\n")
    modules_loaded = False
    exit(1)

# Initialize modules
print("🔧 Initializing modules...\n")

scheduler = NotificationScheduler()
message_gen = MessageGenerator()
state_manager = StateManager()
dispatcher = NotificationDispatcher(enable_desktop=True)

print("✅ Modules initialized!\n")
print("="*70 + "\n")

# Create test invoices with full datetime
print("📋 Creating test invoices with enhanced time...\n")

test_invoices = [
    {
        "invoice_id": "TEST-001",
        "client_name": "Tomorrow Client",
        "amount": 50000,
        "invoice_datetime": (datetime.now() - timedelta(days=44)).isoformat(),
        "deadline_days": 45,
        "paid": False
    },
    {
        "invoice_id": "TEST-002",
        "client_name": "Today Client", 
        "amount": 75000,
        "invoice_datetime": (datetime.now() - timedelta(days=44, hours=20)).isoformat(),
        "deadline_days": 45,
        "paid": False
    },
    {
        "invoice_id": "TEST-003",
        "client_name": "Overdue Client",
        "amount": 30000,
        "invoice_datetime": (datetime.now() - timedelta(days=46)).isoformat(),
        "deadline_days": 45,
        "paid": False
    }
]

# Save to temp file
with open('test_invoices_enhanced.json', 'w') as f:
    json.dump(test_invoices, f, indent=2)

print(f"✅ Created {len(test_invoices)} test invoices\n")

# Load with enhanced monitor
invoice_monitor = InvoiceMonitor("test_invoices_enhanced.json")
invoices_with_time = invoice_monitor.get_invoices_needing_notification()

print("📊 Invoice Details:\n")

for inv in invoices_with_time:
    print(f"  {inv['invoice_id']}: {inv['client_name']}")
    print(f"    Days: {inv['days_left']}, Hours: {inv['hours_left']}")
    print(f"    Status: {inv['human_description']}")

    # Get urgency
    schedule_info = scheduler.get_schedule_info(inv['days_left'], inv['hours_left'], inv['human_description'])
    print(f"    Urgency: {schedule_info['urgency_level']}\n")

print("="*70 + "\n")

# Send notifications with enhanced descriptions
print("🔔 Sending Desktop Notifications...\n")

notifications_sent = 0

for inv in invoices_with_time:
    # Get urgency level
    schedule_info = scheduler.get_schedule_info(inv['days_left'])
    urgency_level = schedule_info['urgency_level']

    # Generate message using enhanced description
    message_data = {
        "invoice_id": inv['invoice_id'],
        "client_name": inv['client_name'],
        "days_left": inv['days_left']
    }

    # Create custom message with enhanced time
    custom_message = f"{inv['client_name']}: {inv['human_description']}"

    print(f"  📤 Sending: {inv['invoice_id']}")
    print(f"     Message: {custom_message}")

    # Send notification
    channels = dispatcher.send_notification(
        message=custom_message,
        urgency_level=urgency_level,
        invoice_data=inv
    )

    if channels:
        notifications_sent += 1
        print(f"     ✅ Sent via: {', '.join(channels)}\n")
    else:
        print(f"     ❌ Failed to send\n")

    time.sleep(2)  # Delay between notifications

print("="*70 + "\n")

# Summary
print("📊 SUMMARY:\n")
print(f"  Total invoices: {len(invoices_with_time)}")
print(f"  Notifications sent: {notifications_sent}")
print(f"  Success rate: {notifications_sent}/{len(invoices_with_time)}\n")

if notifications_sent == 0:
    print("⚠️  No notifications sent! Check:\n")
    print("  1. Is plyer installed? → pip install plyer")
    print("  2. On Linux: sudo pacman -S libnotify")
    print("  3. Try: notify-send 'Test' 'Test message'\n")
else:
    print("✅ Desktop notifications should be visible on your screen!\n")

print("="*70 + "\n")

print("🎯 Enhanced Features Tested:\n")
print("  ✅ Time-based invoice calculations")
print("  ✅ Human-readable descriptions")
print("  ✅ Desktop notification popups")
print("  ✅ Urgency level detection\n")

print("🎉 Test complete!\n")
