"""
Notification Agent - Main orchestrator
Imports and coordinates all modules
"""
import time
from datetime import datetime, timedelta
from scheduler import NotificationScheduler
from message_generator import MessageGenerator
from state_manager import StateManager
from invoice_monitor import InvoiceMonitor
from notification_dispatcher import NotificationDispatcher

class NotificationAgent:
    """Main agent that orchestrates invoice notification system"""

    def __init__(
        self,
        invoices_file="invoices.json",
        enable_desktop=True,
        enable_whatsapp=False,
        enable_email=False
    ):
        # Initialize all modules
        self.scheduler = NotificationScheduler()
        self.message_gen = MessageGenerator()
        self.state_manager = StateManager()
        self.invoice_monitor = InvoiceMonitor(invoices_file)
        self.dispatcher = NotificationDispatcher(
            enable_desktop=enable_desktop,
            enable_whatsapp=enable_whatsapp,
            enable_email=enable_email
        )

        print("🤖 Notification Agent initialized!")
        print(f"   📊 Scheduler: Ready")
        print(f"   💬 Message Generator: Ready")
        print(f"   📝 State Manager: Ready")
        print(f"   👁️  Invoice Monitor: Ready")
        print(f"   📤 Dispatcher: Desktop={'✓' if enable_desktop else '✗'}, "
              f"WhatsApp={'✓' if enable_whatsapp else '✗'}, "
              f"Email={'✓' if enable_email else '✗'}")

    def process_invoice(self, invoice: dict, user_preferences: dict = None) -> bool:
        """
        Process single invoice and send notification if needed

        Returns:
            True if notification was sent
        """
        invoice_id = invoice["invoice_id"]

        # Check if already paid
        if self.state_manager.is_paid(invoice_id):
            return False

        # Check if notifications are disabled
        if not self.state_manager.is_notification_enabled(invoice_id):
            return False

        # Calculate days left and urgency
        days_left = invoice["days_left"]
        schedule_info = self.scheduler.get_schedule_info(days_left)
        urgency_level = schedule_info["urgency_level"]

        # Check if we should notify now
        last_notification = self.state_manager.get_last_notification_time(invoice_id)

        if last_notification:
            should_notify = self.scheduler.should_notify_now(last_notification, urgency_level)
        else:
            should_notify = True  # First notification

        if not should_notify:
            return False

        # Generate message
        message = self.message_gen.generate_message(urgency_level, invoice)

        # Send notification
        channels = self.dispatcher.send_notification(
            message=message,
            urgency_level=urgency_level,
            invoice_data=invoice,
            user_preferences=user_preferences
        )

        # Update state
        if channels:
            self.state_manager.update_notification_sent(
                invoice_id=invoice_id,
                channels=channels,
                urgency_level=urgency_level
            )

            print(f"✅ Notification sent for {invoice_id}")
            print(f"   📍 Urgency: {urgency_level}")
            print(f"   📊 Days left: {days_left}")
            print(f"   📤 Channels: {', '.join(channels)}")
            print(f"   💬 Message: {message[:60]}...")

            return True

        return False

    def run_cycle(self, user_preferences: dict = None):
        """Run one notification check cycle"""
        print(f"\n🔄 Running notification cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Get all active invoices
        invoices = self.invoice_monitor.get_invoices_needing_notification()

        if not invoices:
            print("   ℹ️  No active invoices to monitor")
            return

        print(f"   📋 Found {len(invoices)} active invoice(s)")

        # Process each invoice
        notifications_sent = 0
        for invoice in invoices:
            if self.process_invoice(invoice, user_preferences):
                notifications_sent += 1

        print(f"   ✉️  Sent {notifications_sent} notification(s)")

    def run_daemon(self, check_interval_minutes: int = 30, user_preferences: dict = None):
        """
        Run agent as background daemon

        Args:
            check_interval_minutes: How often to check (default 30 min)
            user_preferences: User contact info and preferences
        """
        print(f"\n🚀 Starting Notification Agent Daemon")
        print(f"   ⏰ Check interval: {check_interval_minutes} minutes")
        print(f"   🔁 Press Ctrl+C to stop\n")

        try:
            while True:
                self.run_cycle(user_preferences)

                # Sleep until next check
                sleep_seconds = check_interval_minutes * 60
                print(f"   😴 Sleeping for {check_interval_minutes} minutes...\n")
                time.sleep(sleep_seconds)

        except KeyboardInterrupt:
            print("\n\n🛑 Notification Agent stopped by user")


# Example usage
if __name__ == "__main__":
    # User preferences (in production, load from Firestore)
    user_prefs = {
        "email": "user@example.com",
        "phone_number": "+1234567890",
        "whatsapp_consent": False  # User must explicitly consent
    }

    # Create agent
    agent = NotificationAgent(
        invoices_file="invoices.json",
        enable_desktop=True,
        enable_whatsapp=False,  # Requires Twilio setup
        enable_email=False      # Requires SMTP setup
    )

    # Run single cycle (for testing)
    agent.run_cycle(user_prefs)

    # Or run as daemon (uncomment to enable)
    # agent.run_daemon(check_interval_minutes=30, user_preferences=user_prefs)
