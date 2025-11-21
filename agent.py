import logging
import os
import sys
from dotenv import load_dotenv

# Import LiveKit Agent Framework
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice import Agent
from livekit.rtc import ParticipantKind

# Import Plugins
from livekit.plugins import openai, deepgram, silero

# 1. Load passwords
load_dotenv()

# FORCE LOGGING TO SCREEN
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("debt-collector")

async def entrypoint(ctx: JobContext):
    logger.info(f"Connecting to room {ctx.room.name}")

    # Connect to the LiveKit Room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # 2. IDENTIFY THE USER (SIP Logic)
    # We wait for the participant (the caller) to join
    participant = await ctx.wait_for_participant()
    
    caller_identity = "Unknown User"
    phone_number = None

    if participant.kind == ParticipantKind.PARTICIPANT_KIND_SIP:
        # It's a phone call!
        phone_number = participant.attributes.get("sip.phoneNumber")
        caller_identity = f"Phone Caller ({phone_number})"
        logger.info(f"📞 INCOMING PHONE CALL DETECTED: {phone_number}")
    else:
        # It's a web browser test
        caller_identity = participant.identity
        logger.info(f"💻 Web Browser User Connected: {caller_identity}")

    # 3. DYNAMIC SYSTEM PROMPT
    # We can inject the phone number into the prompt so the AI knows it.
    system_prompt = f"""
    You are Alex, a professional debt collection agent for 'Summit Credit Services'.
    
    Context:
    - You are speaking with a user via {('phone ' + phone_number) if phone_number else 'web browser'}.
    - If they are on the phone, keep sentences shorter.
    
    Your Goal: 
    1. Verify identity. Ask: "Am I speaking with the account holder associated with this number?"
    2. Inform of $450 balance.
    3. Ask for payment.
    """

    # Create the Agent
    agent = Agent(
        instructions=system_prompt,
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )

    agent.start(ctx.room, participant)
    
    # Greet
    await agent.say("Hello, this is Alex from Summit Credit Services. This call may be recorded.", allow_interruptions=True)

if __name__ == "__main__":
    if not os.getenv("LIVEKIT_URL"):
        print("ERROR: LIVEKIT_URL is missing. Did you create the .env file?")
        sys.exit(1)
        
    print("--------------")
    print("Agent is starting...")
    print("Waiting for calls (SIP or Web)...")
    print("--------------")
    
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))