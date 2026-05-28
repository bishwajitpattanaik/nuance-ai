import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def _download_via_ytdlp(url: str) -> str | None:
    """Try yt-dlp first. Returns wav path on success, None on failure."""
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
        return filename
    except Exception as e:
        print(f"yt-dlp failed: {e}")
        return None


def _download_via_pytubefix(url: str) -> str | None:
    """Fallback to pytubefix. Returns wav path on success, None on failure."""
    try:
        from pytubefix import YouTube
        print("Trying pytubefix fallback...")
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).order_by("abr").last()
        if not stream:
            print("pytubefix: no audio stream found.")
            return None

        raw_path = stream.download(output_path=DOWNLOAD_DIR, filename="yt_audio")
        wav_path = os.path.join(DOWNLOAD_DIR, "yt_audio.wav")
        audio = AudioSegment.from_file(raw_path)
        audio.export(wav_path, format="wav")
        os.remove(raw_path)
        return wav_path
    except Exception as e:
        print(f"pytubefix failed: {e}")
        return None


def download_youtube_audio(url: str) -> str:
    """Try yt-dlp, fall back to pytubefix. Raises if both fail."""
    wav_path = _download_via_ytdlp(url) or _download_via_pytubefix(url)
    if not wav_path:
        raise RuntimeError(
            "Both yt-dlp and pytubefix failed to download the YouTube video.\n"
            "This is likely because Streamlit Cloud's IP is blocked by YouTube.\n"
            "Please download the audio manually and upload the file instead."
        )
    return wav_path


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV (mono, 16kHz)."""
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
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created")
    return chunks