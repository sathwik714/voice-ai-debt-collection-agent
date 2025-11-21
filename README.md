🤖 Voice AI Debt Collection Agent

A real-time, bidirectional voice agent built with LiveKit, OpenAI GPT-4o, and Twilio SIP. This agent handles both inbound and outbound calls, verifies user identity against a database, negotiates debt payments, and logs all interactions for compliance.

🌟 Features

Real-time Conversational AI: Uses LiveKit's WebRTC transport for ultra-low latency (vs. traditional WebSocket bots).

Inbound & Outbound: Can answer calls from debtors or dial out to a list of numbers.

Context Memory: Looks up caller ID in a local database (customers.json) to inject debt details (Balance, Due Date) into the LLM context.

Tool Calling: The AI can "execute" actions like logging a Promise to Pay or Escalating to a Manager.

Analytics: Automatically logs every call disposition and result to call_logs.csv.

Dockerized: Ready for cloud deployment via Docker.

🏗️ Architecture

The system consists of two main processes: the Agent Worker (runs 24/7) and the Dialer (triggers campaigns).

graph TD
    User((Debtor)) <--> PSTN[Twilio SIP]
    PSTN <--> Ingress[LiveKit Cloud]
    Ingress <--> Agent[Python Agent Worker]
    
    Agent -- Reads --> DB[(customers.json)]
    Agent -- Writes --> Logs[call_logs.csv]
    Agent -- Audio --> AI[Deepgram STT / OpenAI LLM / OpenAI TTS]


🛠️ Prerequisites

You need accounts with the following providers:

LiveKit Cloud: For WebRTC/SIP transport.

Twilio: For the phone number and SIP trunking.

OpenAI: For the LLM (GPT-4o) and TTS.

Deepgram: For Speech-to-Text (Nova-2 model).

🚀 Installation

1. Clone & Setup

# Clone repository
git clone [https://github.com/yourusername/debt-collector-agent.git](https://github.com/yourusername/debt-collector-agent.git)
cd debt-collector-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


2. Configuration (.env)

Create a .env file in the root directory:

# LiveKit Keys (Settings -> Keys)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_secret_key

# AI Providers
OPENAI_API_KEY=sk-your-openai-key
DEEPGRAM_API_KEY=your-deepgram-key


3. Mock Database

Ensure customers.json exists in the root. Format:

[
  {
    "phone": "+15551234567",
    "name": "John Doe",
    "balance": 1500.00,
    "days_overdue": 30
  }
]


📞 Usage

Mode A: Receiving Calls (Inbound)

Configure your Twilio SIP Trunk to point to your LiveKit SIP URI.

Start the agent:

python agent.py start


Call your Twilio number. The agent will answer, look up your number in customers.json, and start the negotiation.

Mode B: Campaign Mode (Outbound)

Ensure the Agent is running (step above).

Edit dialer.py and add your LiveKit Outbound Trunk ID.

Run the dialer:

python dialer.py


This script iterates through customers.json, dials each number, and connects them to the running Agent.

🐳 Deployment (Docker)

To run this 24/7 in the cloud (e.g., Fly.io, AWS, Railway):

Build the Image:

docker build -t debt-collector .


Run Locally (Test):

docker run -it --env-file .env debt-collector


📂 Project Structure

File

Description

agent.py

The Brain. Handles connection, AI pipeline, tools, and logging.

dialer.py

The Trigger. Reads DB and creates outbound calls.

customers.json

The Memory. Mock database of user debts.

call_logs.csv

The Report. Generated automatically after calls.

diagnostic.py

The Doctor. Checks API keys and connections.
<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" parent="1" style="whiteSpace=wrap;strokeWidth=2;" value="Agent Orchestrator" vertex="1"><mxGeometry height="54" width="197" x="548" y="681" as="geometry"/></mxCell></root></mxGraphModel>
