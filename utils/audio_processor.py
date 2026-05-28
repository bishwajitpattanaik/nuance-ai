import os
from pydub import AudioSegment

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

SUPPORTED_FORMATS = ["mp3", "mp4", "wav", "m4a", "webm", "ogg", "flac"]


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to mono 16kHz WAV."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Split WAV into chunk_minutes-sized pieces."""
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    """Convert uploaded file to WAV and chunk it."""
    ext = os.path.splitext(source)[-1].lower().strip(".")

    if ext not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format: .{ext}\n"
            f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )

    print(f"Processing uploaded file: {source}")
    wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created")
    return chunks