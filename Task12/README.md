# AI DevOps Agent

A minimal autonomous DevOps AI agent that analyzes a GitHub repository and suggests improvements.

## Features

- Clone GitHub repository
- Detect code smells using flake8
- Detect security vulnerabilities using bandit
- Run tests using pytest
- Use LLM to analyze issues
- Automatically create git branch and commit fixes

## Setup

Install dependencies

pip install -r requirements.txt

Add Groq API key in main.py

Run

python main.py