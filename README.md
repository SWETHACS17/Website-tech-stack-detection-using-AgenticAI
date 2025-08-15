# 🕵️‍♂️ Website Tech Stack Detector using Agentic AI

This project uses **Agentic AI** to analyze any given website URL and detect the underlying **technology stack** — such as frameworks, programming languages, CMS, libraries, and hosting providers.

## 🚀 Features
- Detects frontend frameworks (React, Angular, Vue, etc.)
- Identifies backend technologies (Node.js, Django, PHP, etc.)
- Recognizes hosting/CDN providers (Vercel, Netlify, Cloudflare, etc.)
- Works with any publicly accessible website
- Uses AI reasoning to improve detection accuracy

---

## 📦 Installation

1. **Clone this repository**
   
```bash
git clone https://github.com/SWETHACS17/Website-tech-stack-detection-using-AgenticAI.git
cd /Website-tech-stack-detection-using-AgenticAI
```

2. **Create and activate a virtual environment**
   
Create a .env.local file that contains:
```bash
GROQ_API_KEY=YOUR_GENERATED_GROQ_API_KEY
MODEL=llama-3.1-70b-versatile
```
3. **Dependencies**
```bash
pip install tldextract
pip install groq
pip install requests beautifulsoup4 python-dotenv groq

```

4. **Usage**

Run the script from your terminal:
```bash
python tech_agent.py
```
5. **The program will:**

- Ask you for a website URL (e.g., https://example.com)
- Analyze the page content and metadata
- Print a detailed tech stack report

