
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import re
import textwrap
import tempfile

# Load API key from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Assign a different voice to each speaker
VOICES = {
    "Alex": "alloy",
    "Sam": "onyx"
}


def split_script(script, max_chars=3000):
    """Split long text into smaller chunks."""

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


def parse_dialogue(script):
    """Identify speakers and extract their spoken text."""

    if not isinstance(script, str) or not script.strip():
        raise ValueError("Podcast script cannot be empty.")

    dialogue = []

    # Process each line of the podcast script
    for line_number, line in enumerate(script.splitlines(), start=1):
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Identify Alex or Sam
        match = re.fullmatch(
            r"(Alex|Sam)\s*:\s*(.+)",
            line,
            flags=re.IGNORECASE
        )

        if not match:
            raise ValueError(
                f"Invalid dialogue format in line {line_number}. "
                "Expected 'Alex:' or 'Sam:'."
            )

        speaker = match.group(1).capitalize()
        text = match.group(2).strip()

        if not text:
            raise ValueError(
                f"Empty dialogue in line {line_number}."
            )

        # Split longer speaker contributions
        for chunk in split_script(text):
            dialogue.append((speaker, chunk))

    return dialogue


def generate_audio(script, output_path="outputs/recap.mp3"):
    """Generate a two-speaker podcast as a single MP3 file."""

    # Identify speakers and their dialogue
    dialogue = parse_dialogue(script)

    # Create output folder if needed
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Create empty audio
    combined_audio = AudioSegment.empty()

    # Store individual audio segments temporarily
    with tempfile.TemporaryDirectory() as temp_dir:

        for i, (speaker, text) in enumerate(dialogue):

            # Select voice based on speaker
            voice = VOICES[speaker]

            # Temporary MP3 path
            chunk_path = Path(temp_dir) / f"chunk_{i}.mp3"

            # Generate speech for this speaker
            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text
            ) as response:
                response.stream_to_file(chunk_path)

            # Add segment to the combined podcast
            audio_chunk = AudioSegment.from_mp3(chunk_path)
            combined_audio += audio_chunk

        # Export the complete podcast
        combined_audio.export(output_file, format="mp3")

    # Return file path for Gradio
    return str(output_file)