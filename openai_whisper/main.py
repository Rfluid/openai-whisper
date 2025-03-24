import os
import logging
import tempfile
import argparse
from typing import Optional
from openai import NotGiven, OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def transcribe_audio(
    input_path: str,
    output_path: str,
    batch_size: Optional[int] = None,
    offset: int = 0,
    limit: Optional[int] = None,
    prompt: str | NotGiven = NotGiven(),
):
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        logger.error("OPENAI_API_KEY is not set.")
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI(api_key=openai_api_key)

    # Load audio and apply offset
    audio = AudioSegment.from_file(input_path)
    audio_duration_ms = len(audio)

    offset_ms = offset * 1000
    if offset_ms >= audio_duration_ms:
        raise ValueError("Offset exceeds audio length.")
    audio = audio[offset_ms:]

    if limit:
        limit_ms = limit * 1000
        if limit_ms > len(audio):
            logger.warning(
                "Limit is longer than remaining audio. Using full audio after offset."
            )
        else:
            audio = audio[:limit_ms]

    if batch_size is None:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmpfile:
            audio.export(tmpfile.name, format="mp3")
            with open(tmpfile.name, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    prompt=prompt,
                )
        os.remove(tmpfile.name)

        with open(output_path, "w") as f:
            f.write(transcription)
        print(f"Transcription saved to {output_path}")
        return

    # Batch processing
    print(
        f"Processing in batches of {batch_size} seconds (offset: {offset}, limit: {limit or 'full'})..."
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
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    prompt=prompt,
                )
                full_transcription += transcription + "\n"

        os.remove(tmpfile.name)

    with open(output_path, "w") as f:
        f.write(full_transcription)

    print(f"Full transcription saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio using OpenAI Whisper API."
    )
    parser.add_argument("input_audio_path", help="Path to the input audio file")
    parser.add_argument(
        "output_text_path", help="Path where the transcription will be saved"
    )
    parser.add_argument("--batch-size", type=int, help="Optional batch size in seconds")
    parser.add_argument(
        "--offset", type=int, default=0, help="Seconds to skip from the beginning"
    )
    parser.add_argument(
        "--limit", type=int, help="Maximum duration to transcribe (in seconds)"
    )
    parser.add_argument(
        "--prompt", type=str, help="Prompt to use for the transcription"
    )

    args = parser.parse_args()
    transcribe_audio(
        args.input_audio_path,
        args.output_text_path,
        args.batch_size,
        args.offset,
        args.limit,
        args.prompt,
    )
