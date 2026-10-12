
# ============================================================
# 1. IMPORT OPENAI
# ============================================================

from dotenv import load_dotenv  # Loads variables from .env
from openai import OpenAI       # Imports the OpenAI API client

load_dotenv()                   # Reads OPENAI_API_KEY from .env


# ============================================================
# 2. CREATE THE API CLIENT
# ============================================================

client = OpenAI()
# Create a client object to send requests to OpenAI.
# It automatically looks for the OPENAI_API_KEY environment variable.


# ============================================================
# 3. DEFINE THE SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an experienced educational podcast scriptwriter
who specializes in explaining complex psychological,
philosophical, and spiritual concepts to a general audience.

Your task is to transform a transcript into a clear,
engaging, approximately 5-minute podcast recap.

Instructions:
1. Identify the 5 most important ideas in the transcript.
2. Explain these ideas in a logical, engaging narrative.
3. Preserve the original meaning and important nuances.
4. Remove repetition, filler words, and unnecessary details.
5. Use natural, conversational English suitable for listening.
6. Include a brief introduction, smooth transitions,
   and a meaningful conclusion.
7. Write approximately 700 spoken words, aiming for a
   5-minute podcast at a natural speaking pace.
   Develop the key ideas using details from the source.
   Do not add unsupported examples or repeat ideas
   merely to reach the target length.
8. Present spiritual or astrological interpretations
   as perspectives from the source, not scientific facts.
9. Do not invent information, examples, or claims.
10. Return only the spoken podcast script, without
    headings, timestamps, or production instructions.

The result must be ready for text-to-speech generation.
"""

# SYSTEM_PROMPT contains the instructions for the LLM.
# It defines the ROLE, TASK, STYLE, RULES, and OUTPUT FORMAT.
#
# WHY?
# A specific prompt helps the model generate a useful script
# instead of a generic summary.
#
# Triple quotes """ allow us to write a multiline string.
# Uppercase names are a Python convention for constants.


# ============================================================
# 4. DEFINE THE FUNCTION
# ============================================================

def create_script(transcript):
   
    # create_script = function name used by main.py.
    # transcript = input parameter containing cleaned text.
    
    # INPUT:  transcript (string)
    # OUTPUT: podcast script (string)
    
    # --------------------------------------------------------
    # 4A. VALIDATE THE INPUT
    # --------------------------------------------------------

    if not transcript or not transcript.strip():
        raise ValueError("The transcript cannot be empty.")

    # Prevent sending empty text to the API.
    # .strip() removes spaces and line breaks from the ends.
    # raise ValueError stops execution with a clear error.
    #
    # WHY?
    # Avoid unnecessary API calls and costs.


    # --------------------------------------------------------
    # 4B. SEND ONE REQUEST TO OPENAI
    # --------------------------------------------------------

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=SYSTEM_PROMPT,
        input=transcript
    )


    # --------------------------------------------------------
    # 4C. EXTRACT THE GENERATED TEXT
    # --------------------------------------------------------

    script = response.output_text

    # The API returns a structured response object.
    # .output_text extracts its generated text.
    #

    # --------------------------------------------------------
    # 4D. VALIDATE THE OUTPUT
    # --------------------------------------------------------

    if not script or not script.strip():
        raise ValueError("The LLM returned an empty script.")

    # Check that the model actually returned usable text.
    # This prevents passing an empty script to the TTS module.


    # --------------------------------------------------------
    # 4E. RETURN THE SCRIPT
    # --------------------------------------------------------

    return script.strip()

    # return sends the result back to the calling function.
    # .strip() removes unnecessary spaces at the beginning/end.
    #
    # main.py can then pass this string to:
    # generate_audio(script)
    #
