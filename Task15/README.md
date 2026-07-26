# Autonomous Web Testing AI Agent (Groq Version)

## 🚀 Overview

This project is an AI-powered agent that automatically tests websites for UI and functional issues.

## 🔧 Features

* Website navigation using Playwright
* Broken link detection
* Button validation
* Form testing
* Screenshot capture
* AI-powered bug analysis using Groq (LLaMA 3)

## 🛠 Tech Stack

* Python
* Playwright
* Groq (LLaMA3)
* LangChain (optional structure)

## ▶️ Setup

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Install Playwright browsers:

```
playwright install
```

3. Add your Groq API key in `.env`:

```
GROQ_API_KEY=your_key
```

## ▶️ Run

```
python main.py
```

## 📊 Output

* `report.json`
* Screenshot in `/screenshots`
* AI-generated bug analysis

## 🧠 Future Improvements

* Multi-page crawling
* Login automation
* CI/CD integration
* Visual UI diff testing
