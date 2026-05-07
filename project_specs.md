# Project Specs — AI Voice Assistant

## What the app does and who uses it

This is a self-hosted inbound AI voice agent. When a customer calls a Twilio phone number, the agent:

1. Answers the call automatically
2. Speaks naturally with the customer using AI
3. When the call ends, saves the following to Airtable:
   - Customer phone number
   - Call duration (in seconds)
   - Full transcript of the conversation

**Primary user:** Business owner who wants to automate inbound customer calls.
**End user (caller):** Any customer calling the business phone number.

---

## Tech Stack

| Layer                  | Technology                        |
|------------------------|-----------------------------------|
| Language               | Python 3.9+                       |
| Voice pipeline         | LiveKit Agents (LiveKit Cloud)    |
| Speech-to-Text (STT)   | Deepgram (Nova 2 model)           |
| AI responses (LLM)     | Claude (claude-sonnet-4-6)        |
| Text-to-Speech (TTS)   | ElevenLabs                        |
| Voice Activity Detection | Silero VAD                      |
| Telephony              | Twilio (SIP Trunking)             |
| Database / Logging     | Airtable (REST API)               |
| Hosting                | Hostinger VPS (Ubuntu)            |

---

## External Services

| Service     | What it does                                              | Credentials needed                          |
|-------------|-----------------------------------------------------------|---------------------------------------------|
| LiveKit     | Manages the real-time voice room and agent worker         | `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` |
| Deepgram    | Converts customer speech to text                          | `DEEPGRAM_API_KEY`                          |
| Claude      | Generates natural AI responses                            | `ANTHROPIC_API_KEY`                         |
| ElevenLabs  | Converts AI text responses back to speech                 | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` |
| Twilio      | Provides the phone number; routes calls via SIP to LiveKit | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` |
| Airtable    | Stores call logs (number, duration, transcript)           | `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_NAME` |

---

## User Flow

```
Customer dials Twilio number
        ↓
Twilio routes call via SIP to LiveKit
        ↓
LiveKit Agents worker picks up the call
        ↓
Agent greets the customer (ElevenLabs TTS)
        ↓
Customer speaks → Deepgram converts speech to text
        ↓
OpenAI generates a response
        ↓
ElevenLabs speaks the response to the customer
        ↓
[Loop until customer hangs up]
        ↓
Call ends → agent saves record to Airtable
```

---

## Airtable Data Structure

**Table name:** `Calls`

| Field name    | Type          | Description                                      |
|---------------|---------------|--------------------------------------------------|
| `Phone`       | Phone / Text  | Customer's phone number (e.g. +14155551234)      |
| `Duration`    | Number        | Length of the call in seconds                    |
| `Transcript`  | Long text     | Full conversation text, formatted as dialogue    |
| `Timestamp`   | Date/Time     | When the call started (UTC)                      |

**Example Transcript format:**
```
Customer: Hi, I'd like to know your working hours.
Agent: Hello! Our office is open Monday to Friday, 9am to 6pm.
Customer: Great, thank you.
Agent: You're welcome! Is there anything else I can help you with?
```

---

## File Structure

```
AI VOICE Assistant/
├── agent.py              ← Main voice agent logic (LiveKit worker)
├── airtable_logger.py    ← Function to save call data to Airtable
├── prompts.py            ← System prompt / personality for the AI
├── requirements.txt      ← Python dependencies
├── .env                  ← API keys (never commit to GitHub)
├── .env.example          ← Template showing which keys are needed
├── CLAUDE.md             ← Project rules for Claude Code
├── project_specs.md      ← This file
└── README.md             ← Setup and deployment instructions
```

---

## Definition of Done

The task is complete when:

- [ ] `agent.py` runs without errors (`python agent.py`)
- [ ] Agent successfully connects to LiveKit Cloud as a worker
- [ ] Twilio routes an inbound call to the agent
- [ ] Agent answers the call and greets the customer with voice
- [ ] Customer speech is transcribed correctly by Deepgram
- [ ] Claude generates a relevant response
- [ ] ElevenLabs speaks the response to the customer
- [ ] After the call ends, a new row appears in Airtable with:
  - Correct phone number
  - Correct duration (non-zero)
  - Full transcript of the conversation
  - Correct timestamp
- [ ] No API keys are hardcoded in any `.py` file
- [ ] The agent runs as a background process on the Hostinger VPS (Ubuntu)
