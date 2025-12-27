"""
Message Generator Module - Creates dynamic, non-monotonic notifications
"""
import random
from typing import Dict

class MessageGenerator:
    """Generates varied notification messages based on urgency level"""

    def __init__(self):
        # Message templates for each urgency level
        self.templates = {
            "extreme_calm": [
                "Hey! Invoice #{invoice_id} for {client_name} is due in {days_left} days 📅",
                "Friendly reminder: {client_name}'s invoice needs attention in {days_left} days",
                "Just a heads up: {days_left} days until invoice #{invoice_id} deadline",
                "Invoice #{invoice_id} ({client_name}) - {days_left} days remaining"
            ],
            "calm": [
                "Invoice #{invoice_id} deadline approaching ({days_left} days left)",
                "Time check: {client_name}'s payment is due in {days_left} days ⏰",
                "Reminder: {days_left} days until {client_name} invoice deadline",
                "Hey! {client_name}'s invoice #{invoice_id} needs payment in {days_left} days"
            ],
            "moderate": [
                "⚠️ Invoice #{invoice_id}: {days_left} days remaining!",
                "Action needed: {client_name} payment in {days_left} days",
                "Invoice #{invoice_id} ({client_name}) - {days_left} days left ⚠️",
                "Payment reminder: {client_name} has {days_left} days remaining"
            ],
            "urgent": [
                "🚨 URGENT: Invoice #{invoice_id} due in {days_left} days!",
                "IMMEDIATE ATTENTION: {client_name} payment in {days_left} days 🚨",
                "⚠️ {days_left} days left for invoice #{invoice_id} ({client_name})",
                "Action required: {client_name} invoice deadline in {days_left} days!"
            ],
            "critical": [
                "🔴 CRITICAL: Invoice #{invoice_id} deadline in {days_left} days!",
                "⏰ URGENT: {client_name} payment required in {days_left} days",
                "🚨 Only {days_left} days left for invoice #{invoice_id}!",
                "PAYMENT NEEDED: {client_name} invoice expires in {days_left} days 🔴"
            ],
            "high_critical": [
                "🔴🔴 VERY URGENT: Invoice #{invoice_id} due in {days_left} days!",
                "⚠️⚠️ {days_left} days until {client_name} invoice deadline!",
                "IMMEDIATE ACTION: Invoice #{invoice_id} expires in {days_left} days!",
                "🚨 LAST WARNING: {client_name} payment in {days_left} days 🚨"
            ],
            "explosive": [
                "🔴🔴🔴 CRITICAL: Invoice #{invoice_id} deadline in {days_left} days - PAYMENT REQUIRED NOW!",
                "⏰⏰⏰ LAST CALL: {client_name} invoice expires in {days_left} days!",
                "🚨🚨🚨 EMERGENCY: Invoice #{invoice_id} due in {days_left} days - ACT NOW!",
                "💥 FINAL NOTICE: {client_name} payment MUST be completed in {days_left} days!"
            ]
        }

    def generate_message(self, urgency_level: str, invoice_data: Dict) -> str:
        """
        Generate a random message for the given urgency level

        Args:
            urgency_level: One of the urgency levels
            invoice_data: Dict with invoice_id, client_name, days_left

        Returns:
            Formatted notification message
        """
        templates = self.templates.get(urgency_level, self.templates["extreme_calm"])
        template = random.choice(templates)

        return template.format(
            invoice_id=invoice_data.get("invoice_id", "N/A"),
            client_name=invoice_data.get("client_name", "Client"),
            days_left=invoice_data.get("days_left", 0)
        )

    def generate_multiple_messages(self, urgency_level: str, invoice_data: Dict, count: int = 3) -> list:
        """Generate multiple different messages (useful for testing variety)"""
        messages = []
        templates = self.templates.get(urgency_level, self.templates["extreme_calm"])

        # Shuffle to ensure variety
        shuffled = random.sample(templates, min(count, len(templates)))

        for template in shuffled:
            messages.append(template.format(
                invoice_id=invoice_data.get("invoice_id", "N/A"),
                client_name=invoice_data.get("client_name", "Client"),
                days_left=invoice_data.get("days_left", 0)
            ))

        return messages
