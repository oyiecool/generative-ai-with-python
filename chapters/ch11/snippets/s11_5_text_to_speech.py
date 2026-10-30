from openai import OpenAI

client = OpenAI()
with client.audio.speech.with_streaming_response.create(
    model=s.tts_model, voice="alloy",
    input="Scheduled maintenance begins at 10 p.m. Expect a five-minute VPN interruption.",
) as resp:
    resp.stream_to_file("out/maintenance_notice.mp3")
