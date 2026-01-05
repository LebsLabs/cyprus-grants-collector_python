import requests
from bs4 import BeautifulSoup

url = input("Enter the URL of the webpage to scrape: ")
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

grants = []

# Loop through all <h3> tags (grant names)
for h3 in soup.find_all("h3"):
    grant_name = h3.get_text(strip=True)

    # Get the next paragraph after <h3> for description / amount
    p = h3.find_next("p")
    text = p.get_text(strip=True) if p else ""

    # Extract amount if it contains € or related keywords
    amount = None
    if "€" in text or any(word in text for word in ["Amount", "Funding"]):
        # Very basic extraction: first number after €
        if "€" in text:
            amount = "€" + text.split("€")[1].split()[0]

    grants.append({
        "name": grant_name,
        "text": text,
        "amount": amount
    })

# Print results
# Open a file in write mode
with open("grants.txt", "w", encoding="utf-8") as f:
    for g in grants:
        f.write(f"Grant name: {g['name']}\n")
        f.write(f"Text: {g['text']}\n")
        f.write(f"Amount: {g['amount']}\n")
        f.write("-" * 50 + "\n")  # separator between grants

import os 
os.startfile("grants.txt")
