from utils.audio_processor import process_input
from core.transcriber_whisper import process_all_chunks

#yt video source
source = ""

#extract audio and split into chunks
chunks = process_input(source)

#process chunks for Hindi transcription + English translation
result = process_all_chunks(chunks)

#print Hindi/Hinglish transcript
print("\n========== HINDI TRANSCRIPT ==========\n")
print(result["hindi_transcript"])

#print English translation
print("\n========== ENGLISH TRANSLATION ==========\n")
print(result["english_translation"])