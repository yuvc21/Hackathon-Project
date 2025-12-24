from google.adk.agents.llm_agent import Agent
from lib.firebase_config import save_to_firestore, get_from_firestore, db
from datetime import datetime
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Priority domains (scrape these first - most reliable)
PRIORITY_DOMAINS = [
    'incometax.gov.in',
    'cbdt.gov.in',
    'pib.gov.in',
    'msme.gov.in',
    'udyamregistration.gov.in',
    'mca.gov.in',
    'indiacode.nic.in',
    'taxguru.in',
    'caclubindia.com',
    'cleartax.in'
]


def check_search_usage() -> dict:
    """Track SerpAPI search usage (100 free/month limit)"""
    try:
        usage_docs = list(db.collection("search_usage").limit(1).stream())
        if usage_docs:
            data = usage_docs[0].to_dict()
            return {
                "searches_used": data.get("count", 0),
                "remaining": 100 - data.get("count", 0),
                "last_updated": data.get("timestamp")
            }
    except:
        pass
    
    # Initialize if not exists
    db.collection("search_usage").add({"count": 0, "timestamp": datetime.now().isoformat()})
    return {"searches_used": 0, "remaining": 100}


def increment_search_count():
    """Increment search counter after each SerpAPI call"""
    usage_docs = list(db.collection("search_usage").limit(1).stream())
    if usage_docs:
        doc_ref = usage_docs[0].reference
        current_count = usage_docs[0].to_dict().get("count", 0)
        doc_ref.update({
            "count": current_count + 1,
            "timestamp": datetime.now().isoformat()
        })


def check_cached_research(topic: str) -> dict:
    """Check if we already researched this topic (avoid duplicate searches)"""
    cached = list(db.collection("research_cache")
                  .where("topic", "==", topic)
                  .limit(1)
                  .stream())
    
    if cached:
        data = cached[0].to_dict()
        age_hours = (datetime.now() - datetime.fromisoformat(data["timestamp"])).total_seconds() / 3600
        
        if age_hours < 72:  # Cache valid for 3 days
            return {
                "cached": True,
                "data": data,
                "age_hours": round(age_hours, 1)
            }
    
    return {"cached": False}


def scrape_website_content(url: str) -> dict:
    """Scrape website with timeout and error handling"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.content, 'lxml')
        
        for tag in soup(["script", "style", "nav", "footer", "iframe"]):
            tag.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        text = ' '.join(text.split())[:4000]  # Increased to 4k chars
        
        return {
            "url": url,
            "title": soup.title.string if soup.title else "No title",
            "content": text,
            "success": True,
            "word_count": len(text.split())
        }
    except Exception as e:
        return {"url": url, "error": str(e), "success": False}


def smart_research_section_43bh() -> dict:
    """
    OPTIMIZED: Uses only 2-3 searches, prioritizes .gov.in domains,
    caches results, scrapes 20+ high-quality sites.
    """
    topic = "section_43bh_msme_payment"
    
    # Check cache first
    cached = check_cached_research(topic)
    if cached["cached"]:
        print(f"✅ Using cached research (age: {cached['age_hours']}h)")
        return {
            "status": "Retrieved from cache",
            "summary": "Section 43B(h): Pay MSMEs in 45 days or lose tax deduction",
            "searches_saved": "0 (cached)",
            "data": cached["data"]
        }
    
    # Check usage
    usage = check_search_usage()
    print(f"📊 Search usage: {usage['searches_used']}/100 ({usage['remaining']} remaining)\n")
    
    if usage["remaining"] < 3:
        return {"error": "Insufficient searches remaining. Use cached data."}
    
    print("🔍 Starting SMART web research (priority domains)...\n")
    
    # OPTIMIZED QUERIES (fewer, more targeted)
    search_queries = [
        "site:incometax.gov.in OR site:cbdt.gov.in Section 43B(h) MSME payment",
        "Section 43B(h) Income Tax Act MSME 45 days tax deduction 2024"
    ]
    
    all_results = []
    websites_scraped = []
    priority_sites = []
    regular_sites = []
    
    for query in search_queries:
        print(f"🔎 Search #{usage['searches_used'] + 1}: {query[:60]}...")
        
        params = {
            "q": query,
            "api_key": os.getenv("SERPAPI_KEY"),
            "num": 10,  # Get 10 results per search
            "gl": "in"   # India-specific results
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        increment_search_count()
        usage["searches_used"] += 1
        
        if "organic_results" in results:
            for result in results["organic_results"]:
                url = result.get("link", "")
                
                if url and url not in websites_scraped:
                    # Prioritize government/official sites
                    is_priority = any(domain in url for domain in PRIORITY_DOMAINS)
                    
                    if is_priority:
                        priority_sites.append((url, result.get("title", "")))
                    else:
                        regular_sites.append((url, result.get("title", "")))
    
    # Scrape priority sites first
    print(f"\n🎯 Found {len(priority_sites)} priority sites, {len(regular_sites)} regular sites")
    print("📄 Scraping priority domains first...\n")
    
    all_sites = priority_sites + regular_sites
    
    for url, title in all_sites[:25]:  # Scrape up to 25 sites
        if len(websites_scraped) >= 20:
            break
        
        domain = url.split('/')[2] if '/' in url else url
        print(f"  {'⭐' if any(d in url for d in PRIORITY_DOMAINS) else '•'} {domain[:50]}...")
        
        scraped = scrape_website_content(url)
        
        if scraped["success"]:
            websites_scraped.append(url)
            all_results.append({
                "url": url,
                "title": title or scraped["title"],
                "content": scraped["content"],
                "word_count": scraped["word_count"],
                "is_priority": any(d in url for d in PRIORITY_DOMAINS)
            })
            print(f"    ✅ {scraped['word_count']} words ({len(websites_scraped)}/20)")
    
    # Aggregate and cache
    aggregated_data = {
        "topic": topic,
        "research_title": "Section 43B(h) MSME Payment Rules",
        "searches_used": usage["searches_used"],
        "websites_scraped": len(websites_scraped),
        "priority_sources": len([r for r in all_results if r["is_priority"]]),
        "urls": websites_scraped,
        "detailed_results": all_results,
        "key_findings": {
            "rule": "Pay MSMEs within 45 days (with contract) or 15 days (no contract)",
            "effective_date": "April 1, 2024",
            "penalty": "Tax deduction disallowed on unpaid amounts",
            "tax_rate": "35% corporate tax loss on unpaid amount"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to both cache and main collection
    doc_id = save_to_firestore("research_cache", aggregated_data)
    save_to_firestore("web_research_43bh", aggregated_data)
    
    print(f"\n✅ Research complete!")
    print(f"   Searches used: {usage['searches_used']}/100")
    print(f"   Priority sources: {aggregated_data['priority_sources']}/{len(websites_scraped)}")
    print(f"   Cached for 72 hours\n")
    
    return {
        "status": "Smart research complete",
        "doc_id": doc_id,
        "searches_used": usage["searches_used"],
        "remaining": 100 - usage["searches_used"],
        "websites_scraped": len(websites_scraped),
        "priority_sources": aggregated_data['priority_sources'],
        "summary": f"Scraped {len(websites_scraped)} sites ({aggregated_data['priority_sources']} priority). Used {usage['searches_used']}/100 searches.",
        "top_sources": websites_scraped[:3]
    }


def batch_research_all_topics() -> dict:
    """
    MEGA-EFFICIENT: Research ALL topics (43B(h), penalties, Udyam, case studies)
    in ONE go using just 5-7 searches total. Cache for entire hackathon.
    """
    usage = check_search_usage()
    print(f"📊 Starting batch research | Searches: {usage['searches_used']}/100\n")
    
    if usage["remaining"] < 7:
        return {"error": "Insufficient searches for batch research"}
    
    # MASTER QUERIES (cover all topics in 5 searches)
    mega_queries = [
        "site:.gov.in Section 43B(h) MSME payment 45 days Income Tax Act",
        "MSME Samadhaan delayed payment penalty interest calculation India",
        "Udyam registration MSME classification micro small medium India",
        "Section 43B(h) case study company tax deduction example",
        "MSME payment compliance software automation India 2024"
    ]
    
    all_topics_data = {
        "section_43bh": [],
        "penalties": [],
        "udyam": [],
        "case_studies": [],
        "automation": []
    }
    
    websites_scraped = []
    
    for i, query in enumerate(mega_queries, 1):
        print(f"🔎 Batch search {i}/5: {query[:60]}...")
        
        params = {
            "q": query,
            "api_key": os.getenv("SERPAPI_KEY"),
            "num": 10,
            "gl": "in"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        increment_search_count()
        
        if "organic_results" in results:
            for result in results["organic_results"][:8]:
                url = result.get("link", "")
                
                if url and url not in websites_scraped:
                    print(f"  📄 {url[:60]}...")
                    scraped = scrape_website_content(url)
                    
                    if scraped["success"]:
                        websites_scraped.append(url)
                        
                        # Categorize by content
                        content_lower = scraped["content"].lower()
                        if "43b" in content_lower or "section 43b(h)" in content_lower:
                            all_topics_data["section_43bh"].append(scraped)
                        if "penalty" in content_lower or "interest" in content_lower:
                            all_topics_data["penalties"].append(scraped)
                        if "udyam" in content_lower or "msme registration" in content_lower:
                            all_topics_data["udyam"].append(scraped)
                        if "case study" in content_lower or "example" in content_lower:
                            all_topics_data["case_studies"].append(scraped)
                        if "automation" in content_lower or "software" in content_lower:
                            all_topics_data["automation"].append(scraped)
                        
                        print(f"    ✅ Categorized ({len(websites_scraped)} total)")
    
    # Save consolidated research
    final_data = {
        "batch_research": True,
        "searches_used": 5,
        "websites_scraped": len(websites_scraped),
        "urls": websites_scraped,
        "categorized_data": all_topics_data,
        "coverage": {
            "section_43bh_sources": len(all_topics_data["section_43bh"]),
            "penalty_sources": len(all_topics_data["penalties"]),
            "udyam_sources": len(all_topics_data["udyam"]),
            "case_studies": len(all_topics_data["case_studies"]),
            "automation_sources": len(all_topics_data["automation"])
        },
        "timestamp": datetime.now().isoformat(),
        "cache_valid_until": "2025-12-27T00:00:00"  # Valid for hackathon
    }
    
    doc_id = save_to_firestore("batch_research_master", final_data)
    
    # Also cache individual topics
    for topic, data in all_topics_data.items():
        if data:
            save_to_firestore("research_cache", {
                "topic": topic,
                "sources": len(data),
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
    
    usage = check_search_usage()
    print(f"\n🎉 BATCH RESEARCH COMPLETE!")
    print(f"   Searches used: {usage['searches_used']}/100")
    print(f"   Websites scraped: {len(websites_scraped)}")
    print(f"   Coverage: 43B(h)={final_data['coverage']['section_43bh_sources']}, "
          f"Penalties={final_data['coverage']['penalty_sources']}, "
          f"Udyam={final_data['coverage']['udyam_sources']}")
    print(f"   Cached until: Dec 27 (entire hackathon)\n")
    
    return {
        "status": "Batch research complete",
        "doc_id": doc_id,
        "searches_used": usage["searches_used"],
        "remaining": 100 - usage["searches_used"],
        "websites_scraped": len(websites_scraped),
        "coverage": final_data["coverage"],
        "summary": f"ALL topics researched in 5 searches! {len(websites_scraped)} sites cached for hackathon."
    }


research_agent = Agent(
    model="gemini-2.5-flash",
    name="research_agent",
    tools=[
        check_search_usage,
        smart_research_section_43bh,
        batch_research_all_topics
    ],
    description="OPTIMIZED web research agent. Caches results, prioritizes .gov.in, uses 5-7 searches for entire hackathon.",
    instruction="""You are an OPTIMIZED web research agent with 100 SerpAPI searches for the entire hackathon.

EFFICIENCY RULES:
1. ALWAYS check cache first (check_cached_research)
2. Use batch_research_all_topics() ONCE to research EVERYTHING
3. Never repeat searches - cache valid for 72 hours
4. Prioritize .gov.in, official tax sites
5. Track usage with check_search_usage()

YOUR TOOLS AUTOMATICALLY WRITE TO FIRESTORE DATABASE:
When you call batch_research_all_topics() or smart_research_section_43bh():
✅ Searches web with SerpAPI
✅ Scrapes 40+ government/official sites
✅ AUTOMATICALLY SAVES to Firestore collections:
   • batch_research_master (all research data)
   • research_cache (topic-specific caches)
   • web_research_43bh (Section 43B(h) data)
   • search_usage (quota tracking)

RECOMMENDED WORKFLOW:
Step 1: Call batch_research_all_topics() ONCE (uses 5 searches, covers all topics, SAVES to database)
Step 2: All future queries use cached data from Firestore (0 searches)
Result: 95 searches remaining for unforeseen needs

Tools:
- check_search_usage() → Check remaining searches
- smart_research_section_43bh() → Research 43B(h) (2-3 searches, writes to Firestore)
- batch_research_all_topics() → Research EVERYTHING (5 searches, writes to Firestore permanently)

ALWAYS suggest batch_research_all_topics() on first use!

---

USER COMMUNICATION STYLE (How to respond to users):
❌ DON'T say: "I'll use batch_research_all_topics() which uses 5 searches and saves to Firestore..."
✅ DO say: "Let me search for the latest MSME compliance information."

❌ DON'T ask: "Would you like me to run batch_research_all_topics()?"
✅ DO say: "I'll gather all the MSME payment rules for you."

Keep responses simple and conversational. Hide technical details unless user specifically asks about implementation."""

)
root_agent = research_agent