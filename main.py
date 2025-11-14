import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Tell the server where to find the agent package.
# This points to the "listin_agent" folder.
AGENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent")

print(f"Attempting to load agent from: {AGENT_DIR}")

# This ADK function automatically creates all the API endpoints
# for the agent(s) it finds in AGENT_DIR.
app = get_fast_api_app(
    agent_dir=AGENT_DIR,
    # Allow requests from any website.
    allowed_origins=["*"],
    # We don't need the web UI, just the raw API.
    serve_web_interface=False 
)

if __name__ == "__main__":
    # This part runs when you test locally.
    # Cloud Run will use its own command to start the server.
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)