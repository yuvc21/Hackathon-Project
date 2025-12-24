from agents.research_agent.agent import research_agent

def test_all_research_tools():
    """Test all research agent tools"""
    
    print("🔍 Testing Research Agent...\n")
    
    # Test 1: Section 43B(h) research
    print("Researching Section 43B(h)...")
    result1 = research_agent.tools[0]()  # research_section_43bh
    print(f"{result1['summary']}")
    print(f"   Saved to Firestore: {result1['doc_id']}\n")
    
    # Test 2: Penalty calculations
    print("Researching MSME penalties...")
    result2 = research_agent.tools[1]()  # research_msme_penalties
    print(f"{result2['summary']}")
    print(f"   Saved to Firestore: {result2['doc_id']}\n")
    
    # Test 3: Udyam registration
    print("Researching Udyam system...")
    result3 = research_agent.tools[2]()  # research_udyam_registration
    print(f"{result3['summary']}")
    print(f"   Saved to Firestore: {result3['doc_id']}\n")
    
    # Test 4: Retrieve stored data
    print("Retrieving stored research...")
    result4 = research_agent.tools[3]()  # get_stored_compliance_rules
    print(f"Found {result4['compliance_rules_count']} rules, {result4['penalty_data_count']} penalty docs\n")
    
    print("All research tools working! Check Firebase Console.")

if __name__ == "__main__":
    test_all_research_tools()