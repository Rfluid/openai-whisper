# 📝 Audio Transcriber with Whisper API

This Python app transcribes audio files using OpenAI's Whisper model. You can transcribe the full audio at once or split it into smaller batches (e.g., 60 seconds) for more control.

## 🚀 Features

- 🎧 Accepts `.mp3` (or other `pydub`-supported formats) as input
- 🧠 Uses OpenAI Whisper (`whisper-1`) for transcription
- 🔀 Optional `--batch-size` flag to split audio into chunks
- ⏩ Optional `--offset` flag to skip the beginning of the audio
- 🎯 Optional `--limit` flag to restrict the total transcription duration
- 💾 Saves transcription to a plain `.txt` file
- 🔐 Uses `.env` for secure API key management

---

## 📦 Requirements

- Python 3.7+
- [ffmpeg](https://ffmpeg.org/download.html) installed (required by `pydub`)

### Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Usage

```bash
python main.py <input_audio_path> <output_text_path> [--batch-size <seconds>] [--offset <seconds>] [--limit <seconds>]
```

### ✅ Examples

Transcribe the whole file at once:

```bash
python main.py audio.mp3 transcript.txt
```

Transcribe in 60-second batches:

```bash
python main.py audio.mp3 transcript.txt --batch-size 60
```

Skip the first 10 seconds and transcribe the rest:

```bash
python main.py audio.mp3 transcript.txt --offset 10
```

Skip the first 10 seconds and transcribe only the next 30 seconds:

```bash
python main.py audio.mp3 transcript.txt --offset 10 --limit 30
```

Transcribe only the first minute, in two 30-second chunks:

```bash
python main.py audio.mp3 transcript.txt --limit 60 --batch-size 30
```

---

## 🔐 API Key Setup

Create a `.env` file in the root folder and add your OpenAI key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🛠️ Notes

- Batch processing uses `pydub` to split the audio and temporarily stores segments.
- The full transcription is built by merging each segment's result.
- `--offset` is useful to ignore intros, silence, or ads at the start.
- `--limit` helps keep processing time and API usage under control.

---

## 📄 License

MIT — do what you want.
