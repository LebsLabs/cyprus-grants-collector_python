import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time
from datetime import datetime

# Configuration
RES_BASE_URL = "https://resecfund.org.cy"
MINISTRY_OVERVIEW_URL = "https://www.fundingprogrammesportal.gov.cy/en/programs/programmes-of-the-ministry-of-interior/"
DB_NAME = "cyprus_grants_fresh.db"

# RES schemes (individual pages for rich details)
res_scheme_urls = [
    "https://resecfund.org.cy/en/kat_A1_2024",
    "https://resecfund.org.cy/en/kat_A2_2024",
    "https://resecfund.org.cy/en/kat_A3_2024",
    "https://resecfund.org.cy/en/kat_B1_2024",
    "https://resecfund.org.cy/en/kat_B2_2024",
    "https://resecfund.org.cy/en/kat_H1_2025",
    "https://resecfund.org.cy/en/kat_H2_2025",
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

schemes = []

print("Starting full Cyprus grants scrape...\n")
print("1. Scraping RES Fund schemes (detailed pages)...")

for url in res_scheme_urls:
    print(f"   {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"      Failed: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Unknown RES Scheme"

    funding = "Not specified"
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if '€' in text and any(k in text.lower() for k in ['grant', 'per kw', 'maximum']):
            funding = text
            break

    beneficiaries = "Individuals / Households"
    if any(x in url.lower() for x in ['a2', 'b2', 'h2']):
        beneficiaries = "Vulnerable households"

    app_req = "Online application via RES fund portal"
    open_date = "2024-05-21" if "2024" in url else "2025-01-01"
    close_date = "20 December 2025 or until budget exhausted"

    schemes.append({
        "country": "Cyprus",
        "entity_name": "RES and Energy Conservation Fund",
        "logo_url": "",
        "available_calls": title,
        "beneficiaries": beneficiaries,
        "funding_amount": funding,
        "funding_type": "Grant",
        "eligibility_criteria": "Existing dwellings in Cyprus",
        "open_date": open_date,
        "close_date": close_date,
        "application_requirements": app_req,
        "call_links": url,
        "trigger_website": "https://resecfund.org.cy/en/",
        "date_created": open_date,
        "date_updated": datetime.now().strftime("%Y-%m-%d")
    })

    time.sleep(1)

print("\n2. Scraping Ministry of Interior overview for all schemes...")

try:
    response = requests.get(MINISTRY_OVERVIEW_URL, headers=headers, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"   Failed to load overview: {e}")
else:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all scheme cards/links (typically in divs with class containing 'call' or 'program')
    scheme_links = soup.find_all('a', href=True)
    ministry_schemes_found = 0

    for link in scheme_links:
        href = link['href']
        if '/en/call/' in href or '/en/program/' in href:  # Filter to detail/call pages
            detail_url = href if href.startswith('http') else "https://www.fundingprogrammesportal.gov.cy" + href
            title = link.get_text(strip=True)
            if not title or len(title) < 10:  # Skip empty/short
                continue

            # Basic info from list (we can follow detail_url later for more)
            parent = link.find_parent('div') or link
            desc = parent.get_text(strip=True).replace(title, '').strip()[:300]

            # Try to find dates in nearby text
            nearby_text = parent.get_text()
            open_date = close_date = "See details"

            schemes.append({
                "country": "Cyprus",
                "entity_name": "Ministry of Interior",
                "logo_url": "",
                "available_calls": title,
                "beneficiaries": "Varies (individuals, businesses, low-income)",
                "funding_amount": "See scheme details",
                "funding_type": "Grant",
                "eligibility_criteria": desc or "See official guide",
                "open_date": open_date,
                "close_date": close_date,
                "application_requirements": "Online or via district offices",
                "call_links": detail_url,
                "trigger_website": MINISTRY_OVERVIEW_URL,
                "date_created": "2024-2025",
                "date_updated": datetime.now().strftime("%Y-%m-%d")
            })

            ministry_schemes_found += 1
            time.sleep(0.5)

    print(f"   Found and added {ministry_schemes_found} Ministry of Interior schemes from overview.")

# DataFrame
df = pd.DataFrame(schemes)
print(f"\nTotal scraped: {len(df)} schemes (RES + Ministry of Interior)")

# Fresh DB
conn = sqlite3.connect(DB_NAME)
conn.execute('''
CREATE TABLE IF NOT EXISTS grants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT, entity_name TEXT, logo_url TEXT, available_calls TEXT,
    beneficiaries TEXT, funding_amount TEXT, funding_type TEXT,
    eligibility_criteria TEXT, open_date TEXT, close_date TEXT,
    application_requirements TEXT, call_links TEXT, trigger_website TEXT,
    date_created TEXT, date_updated TEXT
);
''')
df.to_sql('grants', conn, if_exists='replace', index=False)
conn.close()

print(f"\nFresh database '{DB_NAME}' created with all discovered schemes! 🚀")
print("Open it in DB Browser — you'll see RES energy grants + Ministry schemes (e.g., Renovate-Rent, business enhancement, older housing plans).")