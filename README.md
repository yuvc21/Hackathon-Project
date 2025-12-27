

# Hackathon-Project

View research data in Firebase Console:
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project → Firestore Database
3. Browse collections:
   - `batch_research_master` - All research data
   - `research_cache` - Topic-specific caches
   - `search_usage` - API quota tracking

_For more examples, please refer to the [Documentation](https://github.com/yourusername/msme-compliance-agent/wiki)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

### Research Agent
- [x] **Batch Research System** - 40+ websites in 5 searches
- [x] **Smart Caching** - 72-hour cache, 95% quota savings
- [x] **Government Source Priority** - .gov.in, cbdt.gov.in prioritized
- [x] **Auto-categorization** - Section 43B(h), penalties, Udyam, cases
- [x] **Google ADK Integration** - Conversational AI interface
- [x] **Firestore Auto-save** - Automatic database writes

### Data Coverage
- [x] Section 43B(h) payment deadlines (45/15 days)
- [x] Tax penalty calculations (35% disallowance)
- [x] Udyam registration verification
- [x] Real-world compliance case studies
- [x] MSME classification criteria

### Efficiency Stats
- **5 searches** cover all topics (vs typical 30+)
- **72-hour caching** = zero searches after initial run
- **40+ websites** scraped per operation
- **95 searches saved** for future needs

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Research agent with SerpAPI integration
- [x] Firestore caching and storage
- [x] Google ADK conversational interface
- [ ] Notification Manager (Phase 2)
    - [ ] Firebase Cloud Messaging integration
    - [ ] Email/SMS alert system
    - [ ] Invoice upload interface
- [ ] Company Dashboard (Phase 3)
    - [ ] Real-time compliance tracking
    - [ ] Payment deadline calendar
    - [ ] Tax impact calculator
- [ ] Multi-language Support
    - [ ] Hindi
# 📋 Invoice Notification System - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Two Types of Agents](#two-types-of-agents)
4. [Core Modules](#core-modules)
5. [Main Functions](#main-functions)
6. [How It Works](#how-it-works)
7. [Setup Guide](#setup-guide)
8. [Usage Examples](#usage-examples)
9. [Troubleshooting](#troubleshooting)

---

## 1. Overview

### What Is This System?

This is an **Intelligent Invoice Notification System** that automatically reminds you about pending invoice payments. Think of it as a smart assistant that:

- **Watches** your unpaid invoices
- **Calculates** how much time is left until payment deadline
- **Sends** you notifications at the right time
- **Adjusts** notification frequency based on urgency

### Why Is It Special?

Instead of saying "Payment due in 1 days" (confusing!), it tells you:
- "⏰ Due tomorrow at 5:00 PM" (clear!)
- "🔴 Overdue since yesterday" (urgent!)
- "📅 Due on Monday at 2:30 PM" (specific!)

---

## 2. System Architecture

### Components Overview

```
┌─────────────────────────────────────────────────────────┐
│                   YOUR SYSTEM                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐        ┌─────────────────┐            │
│  │ invoices.json│───────▶│ Invoice Monitor │            │
│  │ (Your data)  │        │ (Reads invoices)│            │
│  └──────────────┘        └────────┬────────┘            │
│                                   │                     │
│                                   ▼                     │
│                          ┌─────────────────┐            │
│                          │   Scheduler     │            │
│                          │ (Calculates     │            │
│                          │  time & urgency)│            │
│                          └────────┬────────┘            │
│                                   │                     │
│                                   ▼                     │
│  ┌──────────────┐        ┌─────────────────┐            │ 
│  │   Agent      │───────▶│  Dispatcher     │            │
│  │ (AI Brain)   │        │ (Sends alerts)  │            │
│  └──────────────┘        └────────┬────────┘            │
│                                   │                     │
│                                   ▼                     │
│                          ┌─────────────────┐            │
│                          │ Your Desktop    │            │
│                          │ (Notification)  │            │
│                          └─────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### File Structure

```
notification_agent/
├── agent.py                         # ADK Chat Agent (interactive)
├── notification_service.py          # Background Service (automatic)
├── scheduler.py            # Time & Urgency Calculator
├── invoice_monitor.py      # Invoice Data Reader
├── notification_dispatcher.py       # Notification Sender
├── state_manager.py                 # Tracks notification history
├── invoices.json                    # Your invoice data
└── .env                             # API key configuration
```

---

## 3. Two Types of Agents

### Agent #1: ADK Chat Agent (agent.py)

**What it is:** An AI chatbot you can talk to

**How it works:**
1. You start it: `adk web`
2. Open browser: `http://localhost:8000`
3. Chat with it: "Show me pending invoices"
4. It responds: Shows you analysis and can send notifications

**Use cases:**
- Testing the system
- Manually checking invoice status
- Interactive control
- Asking questions about invoices

**Example conversation:**
```
You: Show me all pending invoices
Agent: I found 3 invoices:
       • INV-001: Due tomorrow at 5:00 PM (CRITICAL!)
       • INV-002: Due in 20 days at 2:30 PM
       • INV-003: Overdue since yesterday (URGENT!)

You: Send notification for INV-001
Agent: ✅ Notification sent! Desktop alert shown.
       Message: "🔴🔴🔴 CRITICAL Invoice #INV-001 - 
                Acme Corp: Due tomorrow at 5:00 PM"
```

---

### Agent #2: Background Service (notification_service.py)

**What it is:** An automatic worker that runs 24/7

**How it works:**
1. You start it: `python notification_service.py`
2. It runs continuously in the background
3. Every 15 minutes, it checks all invoices
4. Automatically sends notifications when needed

**Use cases:**
- Production/real-world use
- Automatic reminders
- Set-and-forget operation
- Running on a server

**Example output:**
```
[2025-12-27 16:30:00] Checking invoices...
  📋 Found 3 active invoices
     • INV-001: Due tomorrow at 5:00 PM
     • INV-003: Overdue since yesterday

  📤 Sending: 🔴🔴🔴 CRITICAL Invoice #INV-001...
  ✅ Sent successfully!

  📤 Sending: 🔴🔴🔴 CRITICAL Invoice #INV-003...
  ✅ Sent successfully!

✅ Sent 2 notifications
```

---

## 4. Core Modules

### Module 1: Invoice Monitor (invoice_monitor.py)

**What it does:** Reads and analyzes invoice data

**Key functions:**

#### `get_invoices_needing_notification()`
Loads all unpaid invoices and calculates time info for each.

**Input:** Reads from `invoices.json`
```json
{
  "invoice_id": "INV-001",
  "invoice_datetime": "2025-12-26T17:00:00",
  "deadline_days": 1
}
```

**Output:** Returns enhanced invoice data
```python
{
  "invoice_id": "INV-001",
  "days_left": 0,
  "hours_left": 22,
  "human_description": "🚨 Due today at 5:00 PM"
}
```

**Simple explanation:** Takes raw invoice data and adds helpful time information.

---

### Module 2: Scheduler (scheduler.py)

**What it does:** Calculates urgency and notification timing

**Key functions:**

#### `calculate_days_left_with_time(invoice_datetime, deadline_days)`
Calculates exactly how much time is left.

**Example:**
```python
Input:  invoice_datetime = "2025-12-26T17:00:00"
        deadline_days = 1
Output: days_left = 0
        hours_left = 22
        human_description = "🚨 Due today at 5:00 PM"
```

#### `get_urgency_level(days_left)`
Determines how urgent the invoice is.

**Urgency Scale:**
- **Explosive** (<2 days): Persistent notifications, contact NOW
- **High Critical** (2-5 days): Every 2 hours
- **Critical** (5-10 days): Every 3 hours
- **Urgent** (10-20 days): 5 times per day
- **Moderate** (20-30 days): 4 times per day
- **Calm** (30-40 days): 3 times per day
- **Extreme Calm** (>40 days): 2 times per day

**Example:**
```python
Input:  days_left = 1
Output: urgency_level = "explosive"
```

#### `should_notify_now(last_notification_time, urgency_level, invoice_time)`
Decides if a notification should be sent right now.

**Logic:**
- Checks when last notification was sent
- Considers urgency level
- Aligns with invoice creation time (±15 minutes)
- Respects notification intervals

**Example:**
```python
Last notified: 2 hours ago
Urgency: explosive (every 2 hours)
Invoice time: 5:00 PM
Current time: 5:10 PM (within 15-min window)
Result: YES, send notification now!
```

---

### Module 3: Notification Dispatcher (notification_dispatcher.py)

**What it does:** Sends notifications through different channels

**Key function:**

#### `send_notification(message, urgency_level, invoice_data)`
Sends the actual notification alert.

**Channels:**
- **Desktop notifications** (pop-ups on your computer)
- **Email** (can be added)
- **WhatsApp** (can be added)

**Example:**
```python
Input:  message = "🔴🔴🔴 CRITICAL Invoice #INV-001: Due tomorrow at 5PM"
        urgency_level = "explosive"

Action: Shows desktop notification popup
        Title: "Invoice Reminder"
        Body: "🔴🔴🔴 CRITICAL Invoice #INV-001: Due tomorrow at 5PM"

Output: ["desktop"]  # List of channels used
```

---

### Module 4: State Manager (state_manager.py)

**What it does:** Remembers notification history

**Key functions:**

#### `get_last_notification_time(invoice_id)`
Returns when we last sent a notification for this invoice.

**Example:**
```python
Input:  invoice_id = "INV-001"
Output: 2025-12-27 14:30:00  # Last notification time
```

#### `update_notification_sent(invoice_id, channels, urgency_level)`
Records that we just sent a notification.

**Example:**
```python
Input:  invoice_id = "INV-001"
        channels = ["desktop"]
        urgency_level = "explosive"

Action: Saves to notification_state.json
        {
          "INV-001": {
            "timestamp": "2025-12-27T16:30:00",
            "channels": ["desktop"],
            "urgency_level": "explosive"
          }
        }
```

---

## 5. Main Functions

### Function 1: analyze_invoices()

**Location:** agent.py (ADK Chat Agent)

**What it does:** Analyzes all pending invoices and returns complete report

**Step-by-step process:**

1. **Load invoices**
   ```python
   invoices = invoice_monitor.get_invoices_needing_notification()
   ```

2. **For each invoice, gather data:**
   - Days left
   - Hours left
   - Human description
   - Urgency level
   - Amount
   - Deadline datetime

3. **Return analysis:**
   ```python
   {
     "total_invoices": 3,
     "critical_count": 2,
     "invoices": [
       {
         "invoice_id": "INV-001",
         "client": "Acme Corp",
         "days_left": 0,
         "hours_left": 22,
         "time_description": "🚨 Due today at 5:00 PM",
         "urgency": "explosive",
         "amount": 50000
       },
       ...
     ]
   }
   ```

**When used:** When user asks "show me invoices" or service needs to check status

---

### Function 2: send_notification()

**Location:** agent.py (ADK Chat Agent)

**What it does:** Sends a notification for a specific invoice

**Parameters:**
- `invoice_id`: Which invoice (e.g., "INV-001")
- `client_name`: Customer name (e.g., "Acme Corp")
- `time_description`: Human-readable time (e.g., "Due tomorrow at 5PM")
- `urgency_level`: How urgent (e.g., "explosive")

**Step-by-step process:**

1. **Create message:**
   ```python
   urgency_prefix = "🔴🔴🔴 CRITICAL"
   message = f"{urgency_prefix} Invoice #{invoice_id} - {client_name}: {time_description}"
   # Result: "🔴🔴🔴 CRITICAL Invoice #INV-001 - Acme Corp: Due tomorrow at 5PM"
   ```

2. **Send via dispatcher:**
   ```python
   channels = dispatcher.send_notification(message, urgency_level, invoice_data)
   # Sends desktop notification
   ```

3. **Record in history:**
   ```python
   state_manager.update_notification_sent(invoice_id, channels, urgency_level)
   # Saves that notification was sent
   ```

4. **Return result:**
   ```python
   {
     "success": True,
     "channels": ["desktop"],
     "message": "🔴🔴🔴 CRITICAL Invoice #INV-001...",
     "time_description": "Due tomorrow at 5:00 PM"
   }
   ```

**When used:** When user says "notify me about INV-001" or service decides to send

---

### Function 3: get_notification_strategy()

**Location:** agent.py (ADK Chat Agent)

**What it does:** Recommends notification strategy for an invoice

**Parameters:**
- `invoice_datetime`: When invoice was created
- `deadline_days`: How many days until payment deadline

**Step-by-step process:**

1. **Calculate time info:**
   ```python
   days_left, hours_left, deadline_dt, human_desc = \
       scheduler.calculate_days_left_with_time(invoice_datetime, deadline_days)
   ```

2. **Get schedule info:**
   ```python
   schedule_info = scheduler.get_schedule_info(days_left, hours_left, human_desc)
   ```

3. **Return strategy:**
   ```python
   {
     "urgency_level": "explosive",
     "frequency_per_day": "Persistent",
     "interval_hours": 0,
     "is_persistent": True,
     "time_description": "Due tomorrow at 5:00 PM",
     "days_left": 1,
     "hours_left": 22,
     "recommendation": "🔴 URGENT: Send persistent notifications immediately"
   }
   ```

**When used:** When user asks "what's the strategy for this invoice?"

---

### Function 4: check_and_notify()

**Location:** notification_service.py (Background Service)

**What it does:** Main loop that checks and sends notifications automatically

**Step-by-step process:**

1. **Get all invoices:**
   ```python
   invoices = invoice_monitor.get_invoices_needing_notification()
   ```

2. **For each invoice:**

   a. **Get time info:**
   ```python
   days_left = inv["days_left"]
   time_desc = inv["human_description"]
   ```

   b. **Get urgency:**
   ```python
   urgency_level = scheduler.get_urgency_level(days_left)
   ```

   c. **Check if should notify:**
   ```python
   last_notif_time = state_manager.get_last_notification_time(invoice_id)
   should_notify = scheduler.should_notify_now(last_notif_time, urgency_level, invoice_dt)
   ```

   d. **If yes, send notification:**
   ```python
   if should_notify:
       message = f"🔴🔴🔴 CRITICAL Invoice #{invoice_id}: {time_desc}"
       dispatcher.send_notification(message, urgency_level, inv)
       state_manager.update_notification_sent(invoice_id, channels, urgency_level)
   ```

3. **Print summary:**
   ```python
   print(f"✅ Sent {notifications_sent} notification(s)")
   ```

**When used:** Runs automatically every 15 minutes in background service

---

## 6. How It Works

### Scenario 1: User Asks About Invoices (ADK Chat Agent)

**User action:** Opens browser, types "Show me all pending invoices"

**System flow:**

1. **AI Agent receives question**
   - Understands user wants to see invoice status

2. **Calls analyze_invoices()**
   - Loads invoice data from invoices.json
   - Invoice Monitor calculates time remaining
   - Scheduler determines urgency levels

3. **Returns analysis**
   ```
   I found 3 pending invoices:

   • INV-001: Acme Corp - 🚨 Due today at 5:00 PM (EXPLOSIVE!)
     Amount: ₹50,000 | Urgency: Critical

   • INV-002: Tech Solutions - 📅 Due in 20 days at 2:30 PM
     Amount: ₹75,000 | Urgency: Moderate

   • INV-003: Quick Client - 🔴 Overdue since yesterday (URGENT!)
     Amount: ₹30,000 | Urgency: Explosive
   ```

4. **User can take action**
   - "Send notification for INV-001"
   - "What's the strategy for INV-003?"

---

### Scenario 2: Automatic Notifications (Background Service)

**Time:** Every 15 minutes

**System flow:**

1. **Timer triggers check_and_notify()**

2. **Load all invoices**
   ```
   [16:30] Checking invoices...
   Found 3 active invoices
   ```

3. **For each invoice:**

   **INV-001 (Due today at 5PM):**
   - Days left: 0
   - Urgency: explosive
   - Last notified: 2 hours ago
   - Should notify: YES (explosive = always notify)
   - Action: Send notification ✅

   **INV-002 (Due in 20 days):**
   - Days left: 20
   - Urgency: moderate (4 times per day = every 6 hours)
   - Last notified: 3 hours ago
   - Should notify: NO (not yet time)
   - Action: Skip

   **INV-003 (Overdue since yesterday):**
   - Days left: -1
   - Urgency: explosive
   - Last notified: 30 minutes ago
   - Should notify: YES (explosive = always notify)
   - Action: Send notification ✅

4. **Send notifications**
   ```
   📤 Sending: 🔴🔴🔴 CRITICAL Invoice #INV-001 - Acme Corp: Due today at 5PM
   ✅ Sent successfully!

   📤 Sending: 🔴🔴🔴 CRITICAL Invoice #INV-003 - Quick Client: Overdue since yesterday
   ✅ Sent successfully!

   ✅ Sent 2 notifications
   ```

5. **Desktop notifications appear:**
   - User sees popup on screen
   - Can click to acknowledge

6. **Wait 15 minutes, repeat**

---

### Scenario 3: Time-Aligned Notifications

**Example:** Invoice created on Jan 25 at 5:00 PM

**Notification schedule:**
- System checks every 15 minutes
- But only sends notifications around 5:00 PM (±15 minutes)
- This aligns with invoice creation time

**Why?** Consistent timing feels natural to users

**Flow:**

```
4:30 PM - Check invoices
         → Time not aligned with 5PM, skip

4:45 PM - Check invoices
         → Within 15-min window of 5PM
         → 2 hours since last notification
         → Send notification! ✅

5:00 PM - Check invoices
         → Just sent 15 min ago, skip

5:15 PM - Check invoices
         → Just sent 30 min ago, skip
```

---

## 7. Setup Guide

### Prerequisites

```bash
# Required software:
- Python 3.8+
- pip (Python package manager)
- Google AI API key (free from ai.google.dev)
```

### Installation Steps

**Step 1: Install Python packages**
```bash
pip install schedule plyer google-adk
```

**Step 2: Set up API key**
```bash
# Create .env file:
cd notification_agent
echo "GOOGLE_AI_API_KEY=your_key_here" > .env
```

**Step 3: Prepare invoice data**
```bash
# Create or update invoices.json with your data
# Format:
{
  "invoice_id": "INV-001",
  "client_name": "Your Client",
  "amount": 50000,
  "invoice_datetime": "2025-12-26T17:00:00",
  "deadline_days": 45,
  "paid": false
}
```

**Step 4: Choose your agent**

**For interactive chat:**
```bash
adk web
# Open http://localhost:8000
```

**For automatic service:**
```bash
python notification_service.py
```

---

## 8. Usage Examples

### Example 1: Check Invoice Status

**Using ADK Chat Agent:**
```
You: Show me all pending invoices

Agent: I found 3 pending invoices:

📊 Summary:
   Total: 3 invoices
   Critical: 2 invoices need immediate attention

1. INV-001 - Acme Corp
   Amount: ₹50,000
   Status: 🚨 Due today at 5:00 PM
   Urgency: EXPLOSIVE 🔴🔴🔴

2. INV-002 - Tech Solutions
   Amount: ₹75,000
   Status: 📅 Due in 20 days at 2:30 PM
   Urgency: Moderate ⚠️

3. INV-003 - Quick Client
   Amount: ₹30,000
   Status: 🔴 Overdue since yesterday
   Urgency: EXPLOSIVE 🔴🔴🔴
```

---

### Example 2: Send Notification

**Using ADK Chat Agent:**
```
You: Send notification for INV-001

Agent: ✅ Notification sent successfully!

📤 Sent via: Desktop notification
💬 Message: "🔴🔴🔴 CRITICAL Invoice #INV-001 - Acme Corp: Due today at 5:00 PM"

The notification has been displayed on your desktop.
Would you like to send notifications for other invoices?
```

---

### Example 3: Get Notification Strategy

**Using ADK Chat Agent:**
```
You: What's the notification strategy for an invoice due in 3 days?

Agent: For an invoice due in 3 days:

⏰ Urgency Level: HIGH CRITICAL 🔴🔴
📊 Notification Frequency: Every 2 hours (12 times per day)
🎯 Strategy: Increase notification frequency. Consider phone call.

Time Description: Due in 3 days at [invoice time]

Recommended actions:
- Send regular notifications every 2 hours
- Prepare follow-up communication
- Monitor payment status closely
- Consider direct contact if no response
```

---

### Example 4: Background Service Running

**Using notification_service.py:**
```bash
$ python notification_service.py

🚀 Starting Notification Service...

✅ Modules initialized:
   📊 Scheduler: Enhanced (with time support)
   👁️  Invoice Monitor: Enhanced (datetime aware)
   📤 Dispatcher: Desktop notifications enabled
   📝 State Manager: Ready

✅ Service started!
⏰ Checking invoices every 15 minutes
📋 Press Ctrl+C to stop
======================================================================

[2025-12-27 16:30:00] Checking invoices...
  📋 Found 3 active invoice(s):
     • INV-001: 🚨 Due today at 5:00 PM
     • INV-002: 📅 Due in 20 days at 2:30 PM
     • INV-003: 🔴 Overdue since yesterday

  📤 Sending: 🔴🔴🔴 CRITICAL Invoice #INV-001 - Acme Corp: Due today at 5:00 PM
  ✅ Sent successfully!

  📤 Sending: 🔴🔴🔴 CRITICAL Invoice #INV-003 - Quick Client: Overdue since yesterday
  ✅ Sent successfully!

✅ Sent 2 notification(s)
======================================================================

[Waiting 15 minutes for next check...]
```

---

## 9. Troubleshooting

### Issue 1: "No module named 'scheduler'"

**Problem:** Enhanced modules not found

**Solution:**
```bash
# Make sure you have these files in notification_agent/ folder:
- scheduler.py
- invoice_monitor.py

# Download them if missing (from earlier in conversation)
```

---

### Issue 2: "Desktop notifications not showing"

**Problem:** Notification library not installed

**Solution:**
```bash
# Install plyer:
pip install plyer

# On Linux, also install libnotify:
sudo pacman -S libnotify  # Arch
sudo apt install libnotify-bin  # Ubuntu

# Test manually:
notify-send "Test" "Hello"
```

---

### Issue 3: "API quota exceeded"

**Problem:** Using experimental model with low quota

**Solution:**
```python
# In agent.py, change model:
model="gemini-1.5-flash"  # Use this (stable, higher quota)
# Not: model="gemini-2.0-flash-exp"  # Experimental, low quota
```

---

### Issue 4: "TypeError: missing positional argument"

**Problem:** Using old version of files

**Solution:**
```bash
# Make sure you're using the latest files:
- agent.py (with time support)
- notification_service.py (final version)

# Check function calls include all parameters:
should_notify_now(last_time, urgency, invoice_time)  # 3 params!
```

---

### Issue 5: Time descriptions not showing

**Problem:** Using old scheduler or invoice monitor

**Solution:**
```bash
# Verify imports in your files:
from scheduler import NotificationScheduler
from invoice_monitor import InvoiceMonitor


```

---

## Summary

This invoice notification system combines:

✅ **Smart time calculation** - Shows "tomorrow at 5PM" not "1 days"
✅ **Urgency detection** - Knows what's critical vs. routine
✅ **Automatic notifications** - Runs 24/7 without your input
✅ **Time alignment** - Sends notifications at consistent times
✅ **Interactive control** - Chat with AI to check status
✅ **Background service** - Set and forget operation

**Two ways to use:**
1. **ADK Chat Agent** - Interactive, for testing and manual control
2. **Background Service** - Automatic, for production use

**Core principle:** Make invoice reminders natural and timely, not annoying!

---

**End of Documentation** 📚

Total words: ~3,500 words
All functions explained with examples
Suitable for non-technical users

See the [open issues](https://github.com/yourusername/msme-compliance-agent/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/yourusername/msme-compliance-agent/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourusername/msme-compliance-agent" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/yourusername/msme-compliance-agent](https://github.com/yourusername/msme-compliance-agent)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Resources and inspirations that made this project possible:

* [Google Agent Development Kit](https://google.github.io/adk-docs/)
* [SerpAPI Documentation](https://serpapi.com/docs)
* [Firebase/Firestore Docs](https://firebase.google.com/docs/firestore)
* [Income Tax Department India](https://incometax.gov.in)
* [MSME Ministry](https://msme.gov.in)
* [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/yourusername/msme-compliance-agent.svg?style=for-the-badge
[contributors-url]: https://github.com/yourusername/msme-compliance-agent/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/yourusername/msme-compliance-agent.svg?style=for-the-badge
[forks-url]: https://github.com/yourusername/msme-compliance-agent/network/members
[stars-shield]: https://img.shields.io/github/stars/yourusername/msme-compliance-agent.svg?style=for-the-badge
[stars-url]: https://github.com/yourusername/msme-compliance-agent/stargazers
[issues-shield]: https://img.shields.io/github/issues/yourusername/msme-compliance-agent.svg?style=for-the-badge
[issues-url]: https://github.com/yourusername/msme-compliance-agent/issues
[license-shield]: https://img.shields.io/github/license/yourusername/msme-compliance-agent.svg?style=for-the-badge
[license-url]: https://github.com/yourusername/msme-compliance-agent/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/yourprofile
[product-screenshot]: https://via.placeholder.com/800x400/1e2327/FFFFFF?text=MSME+Compliance+Agent+Dashboard

[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[ADK.dev]: https://img.shields.io/badge/Google_ADK-4285F4?style=for-the-badge&logo=google&logoColor=white
[ADK-url]: https://google.github.io/adk-docs/
[Gemini.ai]: https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white
[Gemini-url]: https://deepmind.google/technologies/gemini/
[Firebase.com]: https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black
[Firebase-url]: https://firebase.google.com/
[Firestore.dev]: https://img.shields.io/badge/Firestore-FFA611?style=for-the-badge&logo=firebase&logoColor=white
[Firestore-url]: https://firebase.google.com/docs/firestore
[BeautifulSoup.dev]: https://img.shields.io/badge/BeautifulSoup-3776AB?style=for-the-badge&logo=python&logoColor=white
[BeautifulSoup-url]: https://www.crummy.com/software/BeautifulSoup/
