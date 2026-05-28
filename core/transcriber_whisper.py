# import whisper
# import os

# #gets whisper model name from environment or defaults to "small"
# WHISPER_MODEL = os.getenv("WHISPER_MODEL","small")

# #stores the loaded whisper model globally to avoid reloading
# _model = None

# #loads the whisper model once and reuses it for future calls
# def load_model():

#     global _model  #allows _model variable in function scope

#     #loads model only if not already loaded
#     if _model is None: 
#         print(f"Loading Whisper model: {WHISPER_MODEL} ...")
#         _model = whisper.load_model(WHISPER_MODEL) 
#         print("Whisper model loaded successfully")
#     return _model 

# #transcribes an audio chunk file into text using whisper
# def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:

#     model = load_model()  

#     task = "translate" if translate else "transcribe"

#     result = model.transcribe(chunk_path, task = task)  
#     return result["text"]


# #send chunks in loop to transcribe_chunk for transcribing them
# def transcribe_all(chunks: list, translate: bool = False) -> str:

#     full_transcript = ""

#     for i, chunk in enumerate(chunks):
#         print(f"Transcribing chunk {i+1}")

#         text = transcribe_chunk(chunk, translate=translate)

#         full_transcript += text + " "

#     print("Transcription completed")
#     return full_transcript


import whisper
import os

# gets whisper model name from environment or defaults to "small"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

# stores loaded model globally
_model = None


# loads whisper model once
def load_model():

    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded successfully")

    return _model


# transcribes single chunk into Hindi/Hinglish text
def transcribe_chunk(chunk_path: str) -> str:

    model = load_model()

    result = model.transcribe(
        chunk_path,
        language="hi",
        task="transcribe"
    )

    return result["text"]


# translates single chunk into English
def translate_chunk(chunk_path: str) -> str:

    model = load_model()

    result = model.transcribe(
        chunk_path,
        language="hi",
        task="translate"
    )

    return result["text"]


# processes all chunks
def process_all_chunks(chunks: list):

    hindi_transcript = ""
    english_translation = ""

    for i, chunk in enumerate(chunks):

        print(f"Processing chunk {i+1}")

        # Hindi/Hinglish transcription
        hindi_text = transcribe_chunk(chunk)

        # English translation
        english_text = translate_chunk(chunk)

        hindi_transcript += hindi_text + " "
        english_translation += english_text + " "

    print("Processing completed")

    return {
        "hindi_transcript": hindi_transcript,
        "english_translation": english_translation
    }