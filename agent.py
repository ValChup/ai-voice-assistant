import os
import time
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, Agent, AgentSession
from livekit.plugins import deepgram, elevenlabs, anthropic, silero

from prompts import SYSTEM_PROMPT
from airtable_logger import log_call_to_airtable

load_dotenv()


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    phone_number = ctx.room.name
    start_time = time.time()

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=anthropic.LLM(model="claude-sonnet-4-6"),
        tts=elevenlabs.TTS(
            api_key=os.environ["ELEVENLABS_API_KEY"],
            voice_id=os.environ["ELEVENLABS_VOICE_ID"],
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions=SYSTEM_PROMPT),
    )

    await session.generate_reply(
        instructions="Greet the caller and ask how you can help them today."
    )

    await ctx.wait_for_participant()

    duration = int(time.time() - start_time)

    transcript_lines = []
    for item in session.history:
        if not hasattr(item, "role") or not hasattr(item, "content"):
            continue
        text_parts = [c for c in item.content if isinstance(c, str)]
        text = "\n".join(text_parts).strip()
        if text:
            role = "Customer" if item.role == "user" else "Agent"
            transcript_lines.append(f"{role}: {text}")

    transcript = "\n".join(transcript_lines)

    log_call_to_airtable(
        phone=phone_number,
        duration=duration,
        transcript=transcript,
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
