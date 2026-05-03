import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_bidder_info(text):
    prompt = f"""
You are an expert system extracting structured data from bidder documents.

Extract the following fields STRICTLY in JSON format:

{{
  "company_name": "",
  "turnover": "",
  "projects_completed": "",
  "gst_number": "",
  "pan_number": ""
}}

Rules:
- Do NOT add extra text
- If not found, return null
- Keep values exact from text

TEXT:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # 🔥 Remove markdown formatting if present
    if content.startswith("```"):
        content = content.split("```")[1]  # remove first ```
        if content.startswith("json"):
            content = content[4:]  # remove 'json'
        content = content.strip()

    try:
        content = content.strip()

        # Remove markdown wrappers
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        data = json.loads(content)
        return data

    except Exception as e:
        print("⚠️ JSON parsing failed")
        print("Raw output:\n", content)
        return None