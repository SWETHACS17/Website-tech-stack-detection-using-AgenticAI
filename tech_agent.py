import os
import re
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import Dict, List
from groq import Groq

# Load environment variables
load_dotenv(".env.local")  # or just ".env" if that's your file

# ------------------ HTML Fetch ------------------
def fetch_html(url: str) -> str:
    try:
        if not url.startswith("http"):
            url = "https://" + url
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"[Error fetching HTML: {e}]"

# ------------------ Tech Detection ------------------
def detect_tech(html: str) -> Dict[str, List[str]]:
    soup = BeautifulSoup(html, "html.parser")
    clues = {
        "frontend": [],
        "backend": [],
        "database": [],
        "styling": [],
        "payments": [],
        "analytics": [],
        "cdn": [],
        "auth": [],
        "build_tools": [],
        "cms": [],
        "other": []
    }

    text = html.lower()

    # Frontend
    if "react" in text: clues["frontend"].append("React.js")
    if "vue" in text: clues["frontend"].append("Vue.js")
    if "angular" in text: clues["frontend"].append("Angular")
    if "next.js" in text: clues["frontend"].append("Next.js")
    if "svelte" in text: clues["frontend"].append("Svelte")

    # Backend
    if "wp-content" in text: clues["backend"].append("PHP / WordPress")
    if "laravel" in text: clues["backend"].append("Laravel (PHP)")
    if "django" in text: clues["backend"].append("Django (Python)")
    if "flask" in text: clues["backend"].append("Flask (Python)")
    if "express" in text: clues["backend"].append("Express.js (Node.js)")

    # Database
    if "mongodb" in text: clues["database"].append("MongoDB")
    if "postgresql" in text or "pg-" in text: clues["database"].append("PostgreSQL")
    if "mysql" in text: clues["database"].append("MySQL")

    # Styling
    if "bootstrap" in text: clues["styling"].append("Bootstrap CSS")
    if "tailwind" in text: clues["styling"].append("Tailwind CSS")
    if "material-ui" in text: clues["styling"].append("Material UI")

    # Payments
    if "stripe" in text: clues["payments"].append("Stripe")
    if "paypal" in text: clues["payments"].append("PayPal")
    if "razorpay" in text: clues["payments"].append("Razorpay")

    # Analytics
    if "google-analytics" in text or "gtag.js" in text: clues["analytics"].append("Google Analytics")
    if "hotjar" in text: clues["analytics"].append("Hotjar")

    # CDN
    if "cloudflare" in text: clues["cdn"].append("Cloudflare")
    if "akamai" in text: clues["cdn"].append("Akamai")

    # Auth
    if "auth0" in text: clues["auth"].append("Auth0")
    if "firebaseauth" in text: clues["auth"].append("Firebase Auth")

    # Build tools
    if "webpack" in text: clues["build_tools"].append("Webpack")
    if "vite" in text: clues["build_tools"].append("Vite")
    if "gulp" in text: clues["build_tools"].append("Gulp.js")

    # CMS
    if "wp-content" in text: clues["cms"].append("WordPress")
    if "drupal" in text: clues["cms"].append("Drupal")
    if "joomla" in text: clues["cms"].append("Joomla")

    return clues

# ------------------ LLM Summarization ------------------
def llm_summarize(clues: Dict[str, List[str]], url: str, html_sample: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "[Error] GROQ_API_KEY not set in environment."

    try:
        client = Groq(api_key=api_key)
        model = os.getenv("MODEL", "llama-3.1-70b-versatile")

        system_msg = (
            "You are a senior software architect. Given tech clues from a website, "
            "infer the most likely stack. Only state what is supported by evidence; "
            "clearly mark items as 'likely' when inferred. Be concise and structured."
        )

        user_prompt = {
            "url": url,
            "clues": clues,
            "html_sample": html_sample[:200000]
        }

        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {
                    "role": "user",
                    "content": (
                        "Return a clean, human-friendly report with sections:\n"
                        "Frontend, Styling (CSS/UI), Backend (language & framework), CMS/SSG,\n"
                        "Payments, Analytics/Tags, CDN/Performance, Auth, Build Tools, Database (likely),\n"
                        "Other Notable Services.\n\n"
                        "If unknown, say 'Not detected'.\n\n"
                        f"Input JSON: {json.dumps(user_prompt)[:100000]}"
                    ),
                },
            ],
            temperature=0.2,
            max_tokens=1000
        )

        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"[LLM error] {e}"

# ------------------ Main ------------------
if __name__ == "__main__":
    target_url = input("Enter website URL: ").strip()
    html = fetch_html(target_url)
    if html.startswith("[Error"):
        print(html)
    else:
        clues = detect_tech(html)
        print("\n[Detected Clues]")
        print(json.dumps(clues, indent=2))
        print("\n[AI Analysis]")
        print(llm_summarize(clues, target_url, html))
        print("\n[Analysis Complete]")
        
# ------------------ Environment Setup ------------------


