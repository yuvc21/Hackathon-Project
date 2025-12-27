"""
Enhanced Invoice Monitor - With datetime support
"""
from datetime import datetime, timedelta
from typing import List, Dict
import json

class InvoiceMonitor:
    """Monitors invoices with full datetime support"""

    def __init__(self, invoices_file: str = "invoices.json"):
        self.invoices_file = invoices_file

    def load_invoices(self) -> List[Dict]:
        """Load all invoices from data source"""
        try:
            with open(self.invoices_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Invoice file not found: {self.invoices_file}")
            return []

    def get_active_invoices(self) -> List[Dict]:
        """Get all unpaid, active invoices"""
        invoices = self.load_invoices()
        return [inv for inv in invoices if not inv.get("paid", False)]

    def get_invoice_by_id(self, invoice_id: str) -> Dict:
        """Get specific invoice by ID"""
        invoices = self.load_invoices()
        for inv in invoices:
            if inv.get("invoice_id") == invoice_id:
                return inv
        return None

    def calculate_time_info(self, invoice: Dict) -> tuple:
        """
        Calculate complete time information for invoice

        Returns:
            Tuple of (days_left, hours_left, deadline_datetime, human_readable)
        """
        # Get invoice datetime (supports both date and datetime formats)
        invoice_datetime_str = invoice.get("invoice_datetime") or invoice.get("invoice_date")

        # If only date is provided, add default time (9 AM)
        if "T" not in invoice_datetime_str:
            invoice_datetime_str += "T09:00:00"

        invoice_dt = datetime.fromisoformat(invoice_datetime_str)
        deadline_days = invoice.get("deadline_days", 45)

        # Calculate deadline
        deadline_dt = invoice_dt + timedelta(days=deadline_days)

        # Current time
        now = datetime.now()

        # Time difference
        time_diff = deadline_dt - now
        total_seconds = time_diff.total_seconds()

        days_left = int(total_seconds // 86400)
        hours_left = int((total_seconds % 86400) // 3600)

        # Human readable
        human_readable = self._format_time_description(days_left, hours_left, deadline_dt)

        return (days_left, hours_left, deadline_dt, human_readable)

    def _format_time_description(self, days: int, hours: int, deadline: datetime) -> str:
        """Format human-readable time description"""
        if days < 0:
            abs_days = abs(days)
            if abs_days == 0:
                return f"⚠️ Overdue by {abs(hours)} hours"
            elif abs_days == 1:
                return "🔴 Overdue since yesterday"
            else:
                return f"🔴 Overdue by {abs_days} days"
        elif days == 0:
            if hours == 0:
                return "🚨 DUE NOW!"
            else:
                time_str = deadline.strftime("%I:%M %p")
                return f"🚨 Due today at {time_str}"
        elif days == 1:
            time_str = deadline.strftime("%I:%M %p")
            return f"⏰ Due tomorrow at {time_str}"
        elif days == 2:
            time_str = deadline.strftime("%I:%M %p")
            return f"Due day after tomorrow at {time_str}"
        elif days <= 7:
            day_name = deadline.strftime("%A")
            time_str = deadline.strftime("%I:%M %p")
            return f"Due on {day_name} at {time_str}"
        else:
            date_str = deadline.strftime("%b %d, %Y")
            time_str = deadline.strftime("%I:%M %p")
            return f"Due on {date_str} at {time_str}"

    def get_invoices_needing_notification(self) -> List[Dict]:
        """Get all invoices with complete time information"""
        active = self.get_active_invoices()

        for inv in active:
            days, hours, deadline, human = self.calculate_time_info(inv)
            inv["days_left"] = days
            inv["hours_left"] = hours
            inv["deadline_datetime"] = deadline.isoformat()
            inv["human_description"] = human

        return active
