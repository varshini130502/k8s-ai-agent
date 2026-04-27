Advanced Kubernetes AI Copilot (AIOps/ChatOps)

A powerful, highly modular AI-driven tool that translates plain English into exact Kubernetes (`kubectl`) commands, executes them securely, and automatically heals failing commands.

## ✨ Advanced Features
- **Conversational Memory:** Remembers your chat history so you can ask follow-up questions seamlessly.
- **Auto-Fix & Self-Healing:** If a generated command fails (e.g., syntax error or cluster state issue), the AI catches the `stderr`, learns from its mistake, and automatically generates and runs a corrected command up to 3 times.
- **Dual Interfaces:** Use it locally via a terminal CLI, or run it as a Headless Webhook Server (FastAPI) to integrate with Slack or Microsoft Teams.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.x installed
- `kubectl` installed (Optional, but required if you want it to actually query a cluster)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your Free API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create your free API Key.
3. Set the key in your terminal:
   - **Windows (PowerShell):** `$env:GEMINI_API_KEY="your_api_key_here"`
   - **Mac/Linux:** `export GEMINI_API_KEY="your_api_key_here"`

## 💻 How to run it

### Option 1: Interactive CLI Mode (Recommended for Local Use)
Start the interactive Copilot session:
```bash
python k8s_copilot.py
```
You will enter a REPL environment. Try asking:
1. "Find all crashing pods"
2. "Show me the logs for the first one" (It remembers context!)

### Option 2: Webhook Mode (Recommended for Slack/Teams Integration)
Start the FastAPI server:
```bash
python api.py
```
Send an HTTP POST request to the webhook:
```bash
curl -X POST "http://localhost:8000/webhook" -H "Content-Type: application/json" -d "{\"query\": \"Get all namespaces\"}"
```

---
