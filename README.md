# 🎙️ Astrolume – Personalized AI Podcast Generator

## About the App

**Astrolume** is an AI-powered application that creates personalized, two-host podcasts inspired by astrology and personal development.

Using reference material from *The Pattern* about the **Natal Pluto Complex**, the app generates a conversation between two virtual hosts, Alex and Sam, exploring the user's personal question.

The application is built with **Python, OpenAI APIs, and Gradio**.

## What Does It Do?

1. Collects the user's birth date, birth time, birth city, and personal question.
2. Extracts reference information from a PDF about the Natal Pluto Complex.
3. Uses an OpenAI language model to generate a personalized podcast script.
4. Converts the script into speech using two different AI voices.
5. Combines the audio segments into one MP3 podcast.
6. Displays the script and audio player in a Gradio web interface.

**Note:** The app does not calculate a natal chart. Personalization is primarily based on the user's question, while the PDF provides the thematic reference material.

## Project Files

| File | Description |
|---|---|
| `src/data_processor.py` | Extracts and cleans text from the PDF, validates user inputs, and prepares information for the LLM. |
| `src/llm_processor.py` | Uses the OpenAI API to generate a personalized podcast conversation between Alex and Sam. |
| `src/tts_generator.py` | Converts the dialogue into speech using two AI voices and combines the audio into an MP3 file. |
| `src/main.py` | Connects the modules and provides the Gradio interface for generating and listening to podcasts. |
| `requirements.txt` | Lists the Python dependencies needed to run the application. |
| `Pattern-App text .pdf` | Reference document containing information about the Natal Pluto Complex. |

## How to Run

**1. Install dependencies:**

```bash
pip install -r requirements.txt
```

**2. Install FFmpeg**, which is required for combining MP3 audio segments.

**3. Create a `.env` file** in the project root and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

**4. Launch the application:**

```bash
python src/main.py
```

Open the local Gradio URL displayed in the terminal.

## Technologies Used

- **Python** – Application development
- **Gradio** – Interactive web interface
- **OpenAI API** – Podcast script generation and text-to-speech
- **PyMuPDF** – PDF text extraction
- **Pydub + FFmpeg** – Audio processing and MP3 generation

## Project Scope

Astrolume is a bootcamp prototype demonstrating how generative AI, document processing, and text-to-speech can be integrated into an interactive application.

The podcast content is intended for reflection and entertainment, not as a scientifically validated astrological assessment.

Watch the demo here: https://www.loom.com/share/c9b86a2c7ca44b299814c017e30b09c3