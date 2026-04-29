import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import gspread
from google.oauth2.service_account import Credentials
import datetime
import os
import json

# OpenAI setup
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Google Sheets setup using service account
creds_json = os.environ.get("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)

sheet_url = "https://docs.google.com/spreadsheets/d/1EoPdK1gAeNhPQQcLixKECNCneL5gj0svWq5yPgX0jYI/edit?gid=0#gid=0"
sheet = gc.open_by_url(sheet_url)
dashboard = sheet.get_worksheet(0)

print("Connected to Competitive Intelligence Dashboard!")

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        text = " ".join(line for line in lines if line)
        return text[:3000]
    except Exception as e:
        return f"Could not scrape {url}: {str(e)}"

def analyze_competitor(competitor_name, scraped_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a competitive intelligence analyst. You extract clear, actionable insights from competitor content."
                },
                {
                    "role": "user",
                    "content": (
                        f"Analyze this content from {competitor_name} and give me exactly 2 things:\n\n"
                        f"1. SUMMARY: One plain sentence. What is this page actually about? Be specific, not generic.\n"
                        f"2. KEY INSIGHT: One sentence a GTM strategist would find useful. "
                        f"What does this reveal about {competitor_name} positioning, messaging, or go-to-market strategy? Avoid jargon.\n\n"
                        f"Bad example of KEY INSIGHT: They focus on building trust through customer success.\n"
                        f"Good example of KEY INSIGHT: Icertis leads with compliance and enterprise risk reduction, "
                        f"not speed or ease of use, suggesting they target legal and procurement teams, not sales.\n\n"
                        f"Content:\n{scraped_text}\n\n"
                        f"Format your response exactly like this:\n"
                        f"SUMMARY: ...\n"
                        f"KEY INSIGHT: ..."
                    )
                }
            ]
        )
        output = response.choices[0].message.content
        lines = output.strip().split('\n')
        summary = next((l.replace('SUMMARY:', '').strip() for l in lines if 'SUMMARY:' in l), '')
        insight = next((l.replace('KEY INSIGHT:', '').strip() for l in lines if 'KEY INSIGHT:' in l), '')
        return summary, insight
    except Exception as e:
        return f"Error: {str(e)}", ""

competitors = [
    {
        "name": "DocuSign",
        "urls": [
            "https://www.docusign.com/blog",
            "https://www.g2.com/products/docusign/reviews"
        ]
    },
    {
        "name": "Conga",
        "urls": [
            "https://conga.com/resources/blog",
            "https://www.g2.com/products/conga-composer/reviews"
        ]
    },
    {
        "name": "Icertis",
        "urls": [
            "https://www.icertis.com/blog",
            "https://www.g2.com/products/icertis/reviews"
        ]
    }
]

def run_intelligence_agent():
    print(f"Running competitive intelligence agent...")
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    for competitor in competitors:
        for url in competitor["urls"]:
            print(f"Scraping {competitor['name']} - {url}")
            text = scrape_website(url)

            if "Could not scrape" in text:
                print(f"  Failed to scrape")
                continue

            summary, insight = analyze_competitor(competitor["name"], text)

            if not summary:
                print(f"  Failed to analyze")
                continue

            dashboard.append_row([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                competitor["name"],
                url,
                summary,
                insight
            ])

            print(f"  Done: {competitor['name']}")

    print("\nAgent run complete! Check your Google Sheet.")

run_intelligence_agent()
