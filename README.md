# AI Voice Assistant

A self-hosted inbound AI voice agent that answers customer phone calls, holds natural conversations, and automatically logs every call to Airtable.

Built with LiveKit Agents, Claude (Anthropic), Deepgram, and ElevenLabs. Deployed on Fly.io.

---

## What it does

- Answers inbound phone calls automatically
- Listens and responds in natural conversational English
- After each call, saves to Airtable:
  - Caller's phone number
  - Call duration (seconds)
  - Full transcript of the conversation
  - Timestamp

---

## Architecture

```
Caller → Twilio (phone number)
       → LiveKit Cloud (real-time voice room)
       → AI Agent (this repo)
            ├── Deepgram   — speech-to-text
            ├── Claude     — AI responses
            └── ElevenLabs — text-to-speech
       → Airtable (call logs)
```

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Voice pipeline | LiveKit Agents 1.5+ |
| Speech-to-Text | Deepgram Nova 3 |
| LLM | Claude claude-sonnet-4-6 (Anthropic) |
| Text-to-Speech | ElevenLabs |
| Voice Activity Detection | Silero VAD |
| Telephony | Twilio SIP Trunking |
| Call logging | Airtable REST API |
| Hosting | Fly.io |

---

## Local setup

**1. Clone the repo**

```bash
git clone https://github.com/ValChup/ai-voice-assistant.git
cd ai-voice-assistant
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys (LiveKit, Deepgram, Anthropic, ElevenLabs, Twilio, Airtable).

**4. Run the agent**

```bash
python agent.py dev
```

**5. Test in browser**

Open [agents-playground.livekit.io](https://agents-playground.livekit.io), connect with your LiveKit credentials, and speak into your microphone.

---

## Deploy to Fly.io

**1. Install Fly CLI and log in**

```bash
# Install
powershell -ExecutionPolicy ByPass -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
flyctl auth login
```

**2. Create the app**

```bash
flyctl launch --no-deploy
```

**3. Set environment secrets**

```bash
flyctl secrets set LIVEKIT_URL="" LIVEKIT_API_KEY="" LIVEKIT_API_SECRET="" \
  DEEPGRAM_API_KEY="" ANTHROPIC_API_KEY="" \
  ELEVENLABS_API_KEY="" ELEVENLABS_VOICE_ID="" \
  AIRTABLE_API_KEY="" AIRTABLE_BASE_ID="" AIRTABLE_TABLE_NAME=""
```

**4. Deploy**

```bash
flyctl deploy
```

---

## Airtable setup

Create a table called `Calls` with these fields:

| Field | Type |
|-------|------|
| Phone | Single line text |
| Duration | Number |
| Transcript | Long text |
| Timestamp | Single line text |

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `LIVEKIT_URL` | Your LiveKit Cloud WebSocket URL |
| `LIVEKIT_API_KEY` | LiveKit API key |
| `LIVEKIT_API_SECRET` | LiveKit API secret |
| `DEEPGRAM_API_KEY` | Deepgram API key |
| `ANTHROPIC_API_KEY` | Anthropic (Claude) API key |
| `ELEVENLABS_API_KEY` | ElevenLabs API key |
| `ELEVENLABS_VOICE_ID` | ElevenLabs voice ID |
| `AIRTABLE_API_KEY` | Airtable Personal Access Token |
| `AIRTABLE_BASE_ID` | Airtable Base ID (starts with `app`) |
| `AIRTABLE_TABLE_NAME` | Airtable table name (default: `Calls`) |
