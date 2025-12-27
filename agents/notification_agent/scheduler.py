"""
Enhanced Scheduler Module - With time support and better day descriptions
"""
from datetime import datetime, timedelta
from typing import Tuple

FREQUENCY_MAP = {
    "extreme_calm": 12 * 3600,
    "calm": 8 * 3600,
    "moderate": 6 * 3600,
    "urgent": 4.8 * 3600,
    "critical": 3 * 3600,
    "high_critical": 2 * 3600,
    "explosive": 0
}

class NotificationScheduler:
    """Determines urgency level and notification frequency with time awareness"""

    def calculate_days_left_with_time(self, invoice_datetime: str, deadline_days: int) -> tuple:
        """
        Calculate days and hours remaining until invoice deadline

        Args:
            invoice_datetime: ISO format datetime string (YYYY-MM-DDTHH:MM:SS)
            deadline_days: Number of days until deadline (45 or 15)

        Returns:
            Tuple of (days_left, hours_left, deadline_datetime, human_readable)
        """
        # Parse invoice datetime
        invoice_dt = datetime.fromisoformat(invoice_datetime)

        # Calculate exact deadline
        deadline_dt = invoice_dt + timedelta(days=deadline_days)

        # Current time
        now = datetime.now()

        # Time difference
        time_diff = deadline_dt - now

        # Calculate components
        total_seconds = time_diff.total_seconds()
        days_left = int(total_seconds // 86400)
        hours_left = int((total_seconds % 86400) // 3600)

        # Human readable description
        human_readable = self._get_human_time_description(days_left, hours_left, now, deadline_dt)

        return (days_left, hours_left, deadline_dt, human_readable)

    def _get_human_time_description(self, days: int, hours: int, now: datetime, deadline: datetime) -> str:
        """Generate human-readable time description"""

        # Overdue
        if days < 0:
            abs_days = abs(days)
            if abs_days == 0:
                return f"Overdue by {abs(hours)} hours"
            elif abs_days == 1:
                return "Overdue since yesterday"
            elif abs_days == 2:
                return "Overdue since 2 days ago"
            else:
                return f"Overdue by {abs_days} days"

        # Today
        elif days == 0:
            if hours == 0:
                return "Due NOW!"
            elif hours == 1:
                return "Due in 1 hour"
            else:
                return f"Due today in {hours} hours"

        # Tomorrow
        elif days == 1:
            deadline_time = deadline.strftime("%I:%M %p")
            return f"Due tomorrow at {deadline_time}"

        # Day after tomorrow
        elif days == 2:
            deadline_time = deadline.strftime("%I:%M %p")
            return f"Due day after tomorrow at {deadline_time}"

        # Within a week
        elif days <= 7:
            day_name = deadline.strftime("%A")  # Monday, Tuesday, etc.
            time_str = deadline.strftime("%I:%M %p")
            return f"Due on {day_name} at {time_str}"

        # More than a week
        else:
            date_str = deadline.strftime("%b %d")  # Jan 25
            time_str = deadline.strftime("%I:%M %p")
            return f"Due on {date_str} at {time_str} ({days} days)"

    def get_urgency_level(self, days_left: int) -> str:
        """Determine urgency level based on days remaining"""
        if days_left > 40:
            return "extreme_calm"
        elif 30 <= days_left <= 40:
            return "calm"
        elif 20 <= days_left < 30:
            return "moderate"
        elif 10 < days_left < 20:
            return "urgent"
        elif 5 < days_left <= 10:
            return "critical"
        elif 2 < days_left <= 5:
            return "high_critical"
        else:
            return "explosive"

    def get_notification_interval(self, urgency_level: str) -> float:
        """Get notification interval in seconds"""
        return FREQUENCY_MAP.get(urgency_level, 12 * 3600)

    def should_notify_now(self, last_notification_time: datetime, 
                          urgency_level: str, invoice_time: datetime) -> bool:
        """
        Check if notification should be sent now (considering exact time)

        Args:
            last_notification_time: When last notification was sent
            urgency_level: Current urgency level
            invoice_time: Original invoice creation time
        """
        interval = self.get_notification_interval(urgency_level)

        # Explosive mode: always notify
        if urgency_level == "explosive":
            return True

        # First notification
        if last_notification_time is None:
            return True

        # Check time-based alignment for regular notifications
        # Notification should align with invoice creation time
        now = datetime.now()
        time_since_last = (now - last_notification_time).total_seconds()

        # Check if enough time has passed
        if time_since_last < interval:
            return False

        # Check if current time is close to invoice time (within 15 min window)
        invoice_hour = invoice_time.hour
        invoice_minute = invoice_time.minute
        current_hour = now.hour
        current_minute = now.minute

        # Calculate time difference in minutes
        time_diff = abs((current_hour * 60 + current_minute) - (invoice_hour * 60 + invoice_minute))

        # Allow 15-minute window for alignment
        if time_diff <= 15 or time_diff >= (24 * 60 - 15):
            return True

        return False

    def get_schedule_info(self, days_left: int, hours_left: int = 0, 
                          human_description: str = "") -> dict:
        """Get complete scheduling information"""
        urgency = self.get_urgency_level(days_left)
        interval = self.get_notification_interval(urgency)

        if interval > 0:
            notifications_per_day = round(86400 / interval, 1)
        else:
            notifications_per_day = "Persistent"

        return {
            "days_left": days_left,
            "hours_left": hours_left,
            "urgency_level": urgency,
            "interval_seconds": interval,
            "interval_hours": round(interval / 3600, 2),
            "notifications_per_day": notifications_per_day,
            "is_persistent": urgency == "explosive",
            "human_description": human_description or f"{days_left} days left"
        }
