
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
        parts = textwrap.wrap(
            sentence,
            width=max_chars,
            break_long_words=False,
            break_on_hyphens=False
        )

        for part in parts:
            combined = f"{current_chunk} {part}".strip()

            if len(combined) <= max_chars:
                current_chunk = combined
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = part

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def parse_dialogue(script):
    """Identify Alex and Sam and extract their spoken text."""

    if not isinstance(script, str) or not script.strip():
        raise ValueError("Podcast script cannot be empty.")

    dialogue = []

    # Process each line of the podcast script
    for line_number, line in enumerate(
        script.splitlines(), start=1
    ):

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # UPDATED: Allow spaces around the speaker label
        # and recognize Alex/Sam regardless of capitalization
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

    # UPDATED: Add a short pause between speaker turns
    pause = AudioSegment.silent(duration=300)

    # Store individual audio segments temporarily
    with tempfile.TemporaryDirectory() as temp_dir:

        for i, (speaker, text) in enumerate(dialogue):

            # Select voice based on speaker
            voice = VOICES[speaker]

            # Temporary MP3 path
            chunk_path = Path(temp_dir) / f"chunk_{i}.mp3"

            # Generate speech for this speaker
            with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice=voice,
                input=text,
                response_format="mp3"
            ) as response:
                response.stream_to_file(chunk_path)

            # Load the generated MP3
            audio_chunk = AudioSegment.from_mp3(chunk_path)

            # Append audio and a short pause
            combined_audio += audio_chunk + pause

        # Export the complete podcast
        combined_audio.export(output_file, format="mp3")

    # Return file path for Gradio
    return str(output_file)