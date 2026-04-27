from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core import K8sAgent
import uvicorn

app = FastAPI(title="K8s AI Copilot Webhook")

# We instantiate the agent globally. It will maintain memory across requests!
# For production, you might want to map session IDs to separate agent instances.
agent = None

class WebhookRequest(BaseModel):
    query: str

class WebhookResponse(BaseModel):
    final_command: str
    summary: str
    success: bool

@app.on_event("startup")
def startup_event():
    global agent
    try:
        agent = K8sAgent()
    except ValueError as e:
        print(f"Failed to initialize agent: {e}")

@app.post("/webhook", response_model=WebhookResponse)
def handle_webhook(request: WebhookRequest):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized. Check GEMINI_API_KEY.")
    
    # 1. Generate command
    initial_command = agent.generate_command(request.query)
    
    # 2. Execute with auto-fix (Safe mode usually requires human approval, 
    # but webhooks run headlessly. In production, consider limiting to read-only commands!)
    final_cmd, output, success = agent.execute_with_autofix(initial_command)
    
    # 3. Summarize
    summary = agent.summarize_output(request.query, final_cmd, output)
    
    return WebhookResponse(
        final_command=final_cmd,
        summary=summary,
        success=success
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
