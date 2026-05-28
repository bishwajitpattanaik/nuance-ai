from dotenv import load_dotenv
load_dotenv()

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
import os

print("KEY LOADED:", os.getenv("SARVAM_API_KEY"))
print("CWD:", os.getcwd())

#yt video source
source = ""

language = "hinglish"

chunks = process_input(source)

transcript = transcribe_all(
    chunks,
    language=language
)

print("\n=== TRANSCRIPT ===\n")
print(transcript)