from setuptools import setup, find_packages

setup(
    name="openai-whisper",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydub",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "openai-whisper=openai_whisper.main:main",
        ],
    },
    author="Ruy Vieira",
    description="A simple CLI to transcribe audio using OpenAI Whisper.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.7",
)
