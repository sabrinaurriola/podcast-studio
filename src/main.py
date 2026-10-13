
from pathlib import Path
from uuid import uuid4

import gradio as gr

# Import functions from the other files in src/
from data_processor import read_pdf, prepare_podcast_input
from llm_processor import create_script
from tts_generator import generate_audio, parse_dialogue


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

# main.py is inside src/, so go one folder up
# to reach the podcast-studio project folder.
BASE_DIR = Path(__file__).resolve().parent.parent

# The PDF is located in the project root.
# Keep the exact filename, including the space before .pdf.
PDF_PATH = BASE_DIR / "Pattern-App text .pdf"

# Store generated podcasts in the outputs/ folder.
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD THE PDF
# --------------------------------------------------

# Load the reference material once when the app starts.
# Every podcast uses the same Pluto PDF.
pdf_context = read_pdf(PDF_PATH)


# --------------------------------------------------
# 3. GENERATE THE PERSONALIZED PODCAST
# --------------------------------------------------

def generate_personalized_podcast(
    birth_date,
    birth_time,
    birth_city,
    personal_question
):
    """
    Generate a personalized two-host podcast.

    Workflow:
    1. Validate and prepare user information.
    2. Generate a podcast script with OpenAI.
    3. Check that the dialogue follows the correct format.
    4. Generate a two-voice MP3.
    5. Return the script and audio file to Gradio.
    """

    try:
        # Step 1: Prepare the user information and PDF context.
        podcast_context = prepare_podcast_input(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_city=birth_city,
            personal_question=personal_question,
            pdf_context=pdf_context
        )

        # Step 2: Generate the podcast conversation.
        # The output should use Alex: and Sam: speaker labels.
        script = create_script(podcast_context)

        # Step 3: Verify that the TTS module can parse the script.
        dialogue = parse_dialogue(script)

        # Make sure both hosts have speaking turns.
        speakers = {speaker for speaker, text in dialogue}

        if not {"Alex", "Sam"}.issubset(speakers):
            raise ValueError(
                "The generated script must include both Alex and Sam."
            )

        # Step 4: Create a unique filename for each podcast.
        # This avoids overwriting previous generated files.
        audio_path = OUTPUT_DIR / f"podcast_{uuid4().hex}.mp3"

        # Step 5: Convert the dialogue into a two-voice MP3.
        generated_audio_path = generate_audio(
            script,
            output_path=str(audio_path)
        )

        # Step 6: Return the script and audio to Gradio.
        return script, generated_audio_path

    except ValueError as error:
        # Display input validation or dialogue-format errors.
        raise gr.Error(str(error))

    except Exception:
        # Avoid exposing API keys or sensitive details in the UI.
        # The original error will still be available for debugging.
        raise gr.Error(
            "Podcast generation failed. "
            "Check the terminal for details."
        )


# --------------------------------------------------
# 4. BUILD THE GRADIO INTERFACE
# --------------------------------------------------

with gr.Blocks(title="Astralume: Your Personalized Astrology AI Podcast") as demo:

    gr.Markdown(
        """
        # Personalized Astrology Podcast

        Explore your personal questions through an
        astrology-inspired conversation between **Alex and Sam**.

        The podcast uses reference material from *The Pattern*
        about the **Natal Pluto Complex**.

        **Important:** This application does not calculate your
        natal chart or predict personal characteristics from
        birth information. Personalization is based primarily
        on your question.
        """
    )

    with gr.Row():

        # LEFT COLUMN: USER INPUTS
        with gr.Column():

            birth_date = gr.Textbox(
                label="Birth date",
                placeholder="YYYY-MM-DD"
            )

            birth_time = gr.Textbox(
                label="Birth time",
                placeholder="HH:MM (24-hour format)"
            )

            birth_city = gr.Textbox(
                label="Birth city",
                placeholder="e.g. Madrid, Spain"
            )

            personal_question = gr.Textbox(
                label="Your personal question",
                placeholder=(
                    "Why do I struggle to let go of control "
                    "when my life changes?"
                ),
                lines=4
            )

            generate_button = gr.Button(
                "Generate My Podcast",
                variant="primary"
            )

        # RIGHT COLUMN: PODCAST OUTPUTS
        with gr.Column():

            podcast_script = gr.Textbox(
                label="Your Personalized Podcast Script",
                lines=16,
                interactive=False
            )

            podcast_audio = gr.Audio(
                label="Listen to Your Podcast",
                type="filepath",
                interactive=False
            )

    # Connect the button to the generation function.
    generate_button.click(
        fn=generate_personalized_podcast,
        inputs=[
            birth_date,
            birth_time,
            birth_city,
            personal_question
        ],
        outputs=[
            podcast_script,
            podcast_audio
        ]
    )


# --------------------------------------------------
# 5. LAUNCH THE APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    demo.launch(share=True)

