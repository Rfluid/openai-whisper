# 📝 openai-whisper

This Python app transcribes audio files using OpenAI's Whisper model. You can transcribe the full audio at once or split it into smaller batches with support for skipping and limiting durations.

---

## 🚀 Features

- 🎧 Accepts `.mp3` (or any `pydub`-supported format)
- 🧠 Uses OpenAI Whisper (`whisper-1`) for transcription
- 🔀 Optional `--batch-size` flag to split audio into chunks
- ⏩ Optional `--offset` to skip seconds from the beginning
- 🎯 Optional `--limit` to transcribe only a specific duration
- 💾 Saves transcription to a plain `.txt` file
- 🔐 Uses `.env` for secure API key management

---

## 📦 Requirements

- Python 3.7+
- [ffmpeg](https://ffmpeg.org/download.html) installed (required by `pydub`)

Install Python packages:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage

### ✅ Option 1: As a CLI App

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/openai-whisper.git
   cd openai-whisper
   ```

2. Install it locally:

   ```bash
   pip install -e .
   ```

3. Run it from anywhere:

   ```bash
   openai-whisper input.mp3 transcript.txt --batch-size 60 --offset 10 --limit 120
   ```

---

### ✅ Option 2: Run the Raw Script

1. Download the script:

   - `openai_whisper/main.py`

2. Install dependencies:

   ```bash
   pip install openai pydub python-dotenv
   ```

3. Run directly:

   ```bash
   python openai_whisper/main.py input.mp3 transcript.txt --offset 10 --limit 60
   ```

---

## 🔐 API Key Setup

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🧪 Example Commands

Transcribe the whole file:

```bash
openai-whisper ./Fade_to_Black.mp3 ./Fade_to_Black.txt
```

Transcribe in 60-second chunks:

```bash
openai-whisper ./Fade_to_Black.mp3 ./Fade_to_Black.txt --batch-size 60
```

Skip first 10s, limit to 30s:

```bash
openai-whisper ./Fade_to_Black.mp3 ./Fade_to_Black.txt --offset 10 --limit 30
```

Skip first 20s, limit to 65s in 10-second chunks:

```bash
openai-whisper ./Fade_to_Black.mp3 ./Fade_to_Black.txt --batch-size 10 --offset 20 --limit 65
```

---

## 📁 Project Structure

```
openai-whisper/
├── openai_whisper/
│   ├── __init__.py
│   └── main.py
├── .env
├── README.md
├── requirements.txt
├── setup.py
└── pyproject.toml
```

---

## 📄 License

MIT — do what you want.
