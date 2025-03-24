import sys
from openai import OpenAI


def transcribe_audio(input_path, output_path):
    client = OpenAI()

    with open(input_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )

    with open(output_path, "w") as f:
        f.write(transcription)

    print(f"Transcription saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transcribe_audio.py <input_audio_path> <output_text_path>")
        sys.exit(1)

    input_audio_path = sys.argv[1]
    output_text_path = sys.argv[2]

    transcribe_audio(input_audio_path, output_text_path)
