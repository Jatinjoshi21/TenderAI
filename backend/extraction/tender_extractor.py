import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_tender_criteria(text):
    prompt = f"""
You are an expert in analyzing Indian government tenders.

Extract ONLY the following criteria in STRICT JSON:

{{
  "turnover_min": "",
  "projects_min": "",
  "gst_required": "",
  "pan_required": ""
}}

Rules:
- Convert values clearly (e.g., Rs 5 Cr → 5 Cr)
- gst_required → true/false
- pan_required → true/false
- If not found, return null
- DO NOT use markdown

TEXT:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Clean markdown if exists
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        return json.loads(content)
    except:
        print("⚠️ Tender JSON parsing failed")
        print(content)
        return None