import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import tempfile
import argparse

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def transcribe_audio(input_path, output_path, batch_size=None, offset=0):
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        logger.error("OPENAI_API_KEY is not set.")
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI(api_key=openai_api_key)

    # Load audio and apply offset
    audio = AudioSegment.from_file(input_path)
    offset_ms = offset * 1000
    if offset_ms >= len(audio):
        raise ValueError("Offset exceeds audio length.")
    audio = audio[offset_ms:]

    if batch_size is None:
        # Simple transcription (no batching)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmpfile:
            audio.export(tmpfile.name, format="mp3")
            with open(tmpfile.name, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format="text"
                )
        os.remove(tmpfile.name)
        with open(output_path, "w") as f:
            f.write(transcription)
        print(f"Transcription saved to {output_path}")
        return

    # Batch processing
    print(
        f"Processing in batches of {batch_size} seconds (offset: {offset} seconds)..."
    )
    duration_sec = len(audio) / 1000
    batches = int(duration_sec // batch_size) + 1

    full_transcription = ""

    for i in range(batches):
        start = i * batch_size * 1000
        end = min((i + 1) * batch_size * 1000, len(audio))
        chunk = audio[start:end]

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmpfile:
            chunk.export(tmpfile.name, format="mp3")
            with open(tmpfile.name, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format="text"
                )
                full_transcription += transcription + "\n"

        os.remove(tmpfile.name)

    with open(output_path, "w") as f:
        f.write(full_transcription)

    print(f"Full transcription saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe audio using OpenAI Whisper API."
    )
    parser.add_argument("input_audio_path", help="Path to the input audio file")
    parser.add_argument(
        "output_text_path", help="Path where the transcription will be saved"
    )
    parser.add_argument("--batch-size", type=int, help="Optional batch size in seconds")
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Optional offset in seconds to skip from start",
    )

    args = parser.parse_args()
    transcribe_audio(
        args.input_audio_path, args.output_text_path, args.batch_size, args.offset
    )
