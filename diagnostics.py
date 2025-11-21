import sys
import os
import asyncio

# Force immediate output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("[OK] Step 1: Python is working.", flush=True)

# Test Imports
try:
    print("... Importing Modules (this might take a moment)", flush=True)
    from dotenv import load_dotenv
    from livekit import api
    print("[OK] Step 2: Libraries are installed.", flush=True)
except ImportError as e:
    print(f"[ERROR] Missing libraries. {e}", flush=True)
    print("Run: pip install -r requirements.txt", flush=True)
    sys.exit(1)

# Test Keys
load_dotenv()
URL = os.getenv("LIVEKIT_URL")
KEY = os.getenv("LIVEKIT_API_KEY")
SECRET = os.getenv("LIVEKIT_API_SECRET")

if not URL or not KEY or not SECRET:
    print("[ERROR] API Keys are missing in .env file.", flush=True)
    print(f"   URL found: {bool(URL)}", flush=True)
    print(f"   KEY found: {bool(KEY)}", flush=True)
    print(f"   SECRET found: {bool(SECRET)}", flush=True)
    print(f"   URL value: {URL}", flush=True)
    sys.exit(1)
else:
    print("[OK] Step 3: .env file is loaded correctly.", flush=True)

# Test Connection
async def test_connection():
    print(f"... Attempting to connect to: {URL}", flush=True)
    try:
        # Try a simple Room API call to check credentials
        lkapi = api.LiveKitAPI(URL, KEY, SECRET)
        rooms = await lkapi.room.list_rooms(api.ListRoomsRequest())
        print("[OK] Step 4: SUCCESS! Connected to LiveKit Cloud.", flush=True)
        print(f"   Current active rooms: {len(rooms.rooms)}", flush=True)
        await lkapi.aclose()
    except Exception as e:
        print(f"[ERROR] Could not connect to LiveKit.", flush=True)
        print(f"   Reason: {e}", flush=True)
        print("   Hint: Check if your LIVEKIT_URL starts with 'wss://' and your keys are correct.", flush=True)

if __name__ == "__main__":
    asyncio.run(test_connection())
    print("\nIf you see all 4 checks pass, your Agent code should work.", flush=True)
    print("Try running: python agent.py start", flush=True)