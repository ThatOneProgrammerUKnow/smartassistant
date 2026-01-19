import os, requests
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from io import BytesIO


# Configuration
PLAY_SOUNDS = False
SPEECH_TO_TEXT = False

# Initialize ElevenLabs
load_dotenv()
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)


#==========# Public methods #==========#
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

def get_text(filename):
    if SPEECH_TO_TEXT:
        with open(filename, "rb") as f:
            audio_data = BytesIO(f.read())

        transcription = elevenlabs.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1", # Model to use
            language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
            diarize=True, # Whether to annotate who is speaking
        )
        return transcription


    
