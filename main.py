import os
import sys
from openai import OpenAI
import logging
from dotenv import load_dotenv  # Import dotenv to load environment variables


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def transcribe_audio(input_path, output_path):
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        logger.error(
            "OPENAI_API_KEY required environment variable is not set. Please check your environment variables."
        )
        raise ValueError(
            "OPENAI_API_KEY not found. Please set the OPENAI_API_KEY environment variable."
        )

    client = OpenAI(
        api_key=openai_api_key,
    )

    with open(input_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )

    with open(output_path, "w") as f:
        f.write(transcription)

    print(f"Transcription saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_audio_path> <output_text_path>")
        sys.exit(1)

    input_audio_path = sys.argv[1]
    output_text_path = sys.argv[2]

    transcribe_audio(input_audio_path, output_text_path)
