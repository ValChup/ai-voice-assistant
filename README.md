# AI Voice Assistant

An inbound AI voice agent that answers customer calls, converses naturally using AI, and logs call details to Airtable.

## How it works

1. Customer calls your Twilio phone number
2. Twilio routes the call via SIP to LiveKit Cloud
3. The agent answers, listens, and responds using AI
4. After the call ends, the agent saves the phone number, duration, and full transcript to Airtable

## Tech stack

- **Voice pipeline:** LiveKit Agents
- **Speech-to-Text:** Deepgram
- **AI responses:** Claude (claude-sonnet-4-6)
- **Text-to-Speech:** ElevenLabs
- **Telephony:** Twilio (SIP Trunking)
- **Database:** Airtable

## Setup

### 1. Clone the repo and install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up your environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in all your API keys.

### 3. Run locally

```bash
python agent.py dev
```

### 4. Deploy to Hostinger VPS (Ubuntu)

```bash
# SSH into your server
ssh root@your-server-ip

# Install Python and pip if needed
apt update && apt install python3 python3-pip -y

# Upload files and install dependencies
pip install -r requirements.txt

# Run as a background process
nohup python agent.py start &> agent.log &
```

## Airtable setup

Create a table called `Calls` with these fields:

| Field       | Type      |
|-------------|-----------|
| Phone       | Phone     |
| Duration    | Number    |
| Transcript  | Long text |
| Timestamp   | Date/Time |
