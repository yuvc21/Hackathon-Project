from google.adk.agents.root_agent import RootAgent
from agents.risk_agent import root_agent as risk_agent


app = RootAgent(
    name="MSMEComplianceHub",
    model="gemini-2.5-flash",
    agents=[risk_agent],
    instruction=(
        "Central MSME payment compliance assistant. "
        "Use the risk_agent to analyze invoices, "
        "detect 45‑day MSME violations (Section 43B(h)), "
        "and generate payment alerts."
    ),
)