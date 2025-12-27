"""
Notification Dispatcher Module - Sends notifications via multiple channels
"""
import platform
from typing import List, Dict

class NotificationDispatcher:
    """Handles multi-channel notification delivery"""

    def __init__(self, enable_desktop=True, enable_whatsapp=False, enable_email=False):
        self.enable_desktop = enable_desktop
        self.enable_whatsapp = enable_whatsapp
        self.enable_email = enable_email
        self.platform = platform.system()

    def send_desktop_notification(self, title: str, message: str, is_persistent: bool = False) -> bool:
        """
        Send cross-platform desktop notification

        Args:
            title: Notification title
            message: Notification body
            is_persistent: If True, makes notification sticky (<2 days mode)

        Returns:
            True if successful
        """
        try:
            # Try plyer first (cross-platform)
            try:
                from plyer import notification
                notification.notify(
                    title=title,
                    message=message,
                    app_name="Invoice Reminder",
                    timeout=0 if is_persistent else 10
                )
                return True
            except ImportError:
                pass

            # Platform-specific fallbacks
            if self.platform == "Linux":
                import subprocess
                urgency = "critical" if is_persistent else "normal"
                subprocess.run([
                    "notify-send",
                    "-u", urgency,
                    "-t", "0" if is_persistent else "10000",
                    title,
                    message
                ])
                return True

            elif self.platform == "Darwin":  # macOS
                import subprocess
                subprocess.run([
                    "osascript",
                    "-e",
                    f'display notification "{message}" with title "{title}"'
                ])
                return True

            elif self.platform == "Windows":
                # Using win10toast for Windows
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        title,
                        message,
                        duration=None if is_persistent else 10,
                        threaded=True
                    )
                    return True
                except ImportError:
                    print("⚠️  win10toast not installed for Windows notifications")
                    return False

            else:
                print(f"⚠️  Desktop notifications not supported on {self.platform}")
                return False

        except Exception as e:
            print(f"❌ Desktop notification failed: {e}")
            return False

    def send_whatsapp_notification(self, phone_number: str, message: str) -> bool:
        """
        Send WhatsApp notification via Twilio API

        Args:
            phone_number: Recipient phone number (with country code)
            message: Message to send

        Returns:
            True if successful
        """
        if not self.enable_whatsapp:
            return False

        try:
            from twilio.rest import Client
            import os

            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

            if not account_sid or not auth_token:
                print("⚠️  Twilio credentials not configured")
                return False

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_=whatsapp_number,
                body=message,
                to=f"whatsapp:{phone_number}"
            )

            print(f"✅ WhatsApp sent: {message.sid}")
            return True

        except Exception as e:
            print(f"❌ WhatsApp notification failed: {e}")
            return False

    def send_email_notification(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Send email notification via SMTP

        Args:
            recipient_email: Recipient email address
            subject: Email subject
            body: Email body

        Returns:
            True if successful
        """
        if not self.enable_email:
            return False

        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import os

            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            smtp_email = os.getenv("SMTP_EMAIL")
            smtp_password = os.getenv("SMTP_PASSWORD")

            if not smtp_email or not smtp_password:
                print("⚠️  SMTP credentials not configured")
                return False

            msg = MIMEMultipart()
            msg['From'] = smtp_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_email, smtp_password)
                server.send_message(msg)

            print(f"✅ Email sent to {recipient_email}")
            return True

        except Exception as e:
            print(f"❌ Email notification failed: {e}")
            return False

    def send_notification(
        self,
        message: str,
        urgency_level: str,
        invoice_data: Dict,
        user_preferences: Dict = None
    ) -> List[str]:
        """
        Send notification via all enabled channels

        Args:
            message: Notification message
            urgency_level: Urgency level (for persistent mode)
            invoice_data: Invoice details
            user_preferences: User channel preferences and contact info

        Returns:
            List of successful channels
        """
        successful_channels = []
        is_persistent = (urgency_level == "explosive")

        # 1. Desktop notification (always first)
        if self.enable_desktop:
            title = f"Invoice #{invoice_data.get('invoice_id')} Reminder"
            if self.send_desktop_notification(title, message, is_persistent):
                successful_channels.append("desktop")

        # 2. WhatsApp (if user consented and available)
        if user_preferences and user_preferences.get("whatsapp_consent"):
            phone = user_preferences.get("phone_number")
            if phone and self.send_whatsapp_notification(phone, message):
                successful_channels.append("whatsapp")

        # 3. Email (if configured)
        if user_preferences and user_preferences.get("email"):
            email = user_preferences["email"]
            subject = f"Invoice Reminder: #{invoice_data.get('invoice_id')}"
            if self.send_email_notification(email, subject, message):
                successful_channels.append("email")

        return successful_channels
