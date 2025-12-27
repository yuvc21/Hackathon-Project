"""
State Manager Module - Tracks notification history and state
"""
from datetime import datetime
from typing import Dict, Optional
import json

class StateManager:
    """Manages notification state for invoices (in-memory + file persistence)"""

    def __init__(self, state_file: str = "notification_state.json"):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from file"""
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_state(self):
        """Save state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)

    def get_invoice_state(self, invoice_id: str) -> Optional[Dict]:
        """Get state for specific invoice"""
        return self.state.get(invoice_id)

    def update_notification_sent(
        self, 
        invoice_id: str, 
        channels: list,
        urgency_level: str
    ):
        """Record that notification was sent"""
        if invoice_id not in self.state:
            self.state[invoice_id] = {
                "invoice_id": invoice_id,
                "first_notification": datetime.now().isoformat(),
                "last_notification": None,
                "notification_count": 0,
                "channels_used": [],
                "notification_enabled": True,
                "dismissed_count": 0
            }

        # Update state
        self.state[invoice_id]["last_notification"] = datetime.now().isoformat()
        self.state[invoice_id]["notification_count"] += 1
        self.state[invoice_id]["urgency_level"] = urgency_level

        # Track channels
        for channel in channels:
            if channel not in self.state[invoice_id]["channels_used"]:
                self.state[invoice_id]["channels_used"].append(channel)

        self._save_state()

    def get_last_notification_time(self, invoice_id: str) -> Optional[datetime]:
        """Get when last notification was sent"""
        invoice_state = self.get_invoice_state(invoice_id)
        if invoice_state and invoice_state.get("last_notification"):
            return datetime.fromisoformat(invoice_state["last_notification"])
        return None

    def is_notification_enabled(self, invoice_id: str) -> bool:
        """Check if notifications are enabled for this invoice"""
        invoice_state = self.get_invoice_state(invoice_id)
        if invoice_state:
            return invoice_state.get("notification_enabled", True)
        return True

    def disable_notifications(self, invoice_id: str):
        """User turned off notifications"""
        if invoice_id in self.state:
            self.state[invoice_id]["notification_enabled"] = False
            self._save_state()

    def mark_as_paid(self, invoice_id: str):
        """Mark invoice as paid (stops notifications)"""
        if invoice_id in self.state:
            self.state[invoice_id]["paid"] = True
            self.state[invoice_id]["paid_at"] = datetime.now().isoformat()
            self._save_state()

    def is_paid(self, invoice_id: str) -> bool:
        """Check if invoice is marked as paid"""
        invoice_state = self.get_invoice_state(invoice_id)
        return invoice_state.get("paid", False) if invoice_state else False

    def get_notification_count(self, invoice_id: str) -> int:
        """Get total notifications sent for invoice"""
        invoice_state = self.get_invoice_state(invoice_id)
        return invoice_state.get("notification_count", 0) if invoice_state else 0
