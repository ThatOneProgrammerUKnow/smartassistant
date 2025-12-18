import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play


# Configuration
PLAY_SOUNDS = True

# Initialize ElevenLabs
load_dotenv()
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)


def play_sound(text):
    if PLAY_SOUNDS:
        """Convert text to speech and play audio."""
        audio_stream = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        audio_bytes = b"".join(audio_stream)
        play(audio_bytes)
