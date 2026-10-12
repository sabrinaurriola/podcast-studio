
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import re
import textwrap
import tempfile
from pydub import AudioSegment

# Load API key from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def split_script(script, max_chars=3000):
    """Split a long podcast script into smaller text chunks."""

    if not isinstance(script, str) or not script.strip():
        raise ValueError("Podcast script cannot be empty.")

    # Split text into sentences
    sentences = re.split(r"(?<=[.!?])\s+", script.strip())

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Handle sentences longer than the limit
        parts = textwrap.wrap(sentence, width=max_chars)

        for part in parts:
            combined = f"{current_chunk} {part}".strip()

            if len(combined) <= max_chars:
                current_chunk = combined
            else:
                chunks.append(current_chunk)
                current_chunk = part

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def generate_audio(script, output_path="outputs/recap.mp3"):
    """Convert a podcast script into a single MP3 file."""

    # Split script into smaller chunks
    chunks = split_script(script)

    # Create output folder if needed
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Handle short scripts with one API request
    if len(chunks) == 1:
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=chunks[0]
        ) as response:
            response.stream_to_file(output_file)

    # Handle longer scripts with multiple API requests
    else:
        combined_audio = AudioSegment.empty()

        with tempfile.TemporaryDirectory() as temp_dir:
            for i, chunk in enumerate(chunks):
                chunk_path = Path(temp_dir) / f"chunk_{i}.mp3"

                # Generate audio for each chunk
                with client.audio.speech.with_streaming_response.create(
                    model="gpt-4o-mini-tts",
                    voice="alloy",
                    input=chunk
                ) as response:
                    response.stream_to_file(chunk_path)

                # Add chunk to the combined audio
                audio_chunk = AudioSegment.from_mp3(chunk_path)
                combined_audio += audio_chunk

            # Export final podcast
            combined_audio.export(output_file, format="mp3")

    # Return file path for Gradio
    return str(output_file)