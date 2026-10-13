import pymupdf
from datetime import datetime


# ORIGINAL FUNCTION - Keep
def read_transcript(path):
    """
    Read a text file and return its content as a string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ORIGINAL FUNCTION - Keep
def clean_text(text):
    """
    Remove unnecessary whitespace from text.
    """
    return " ".join(text.split())


# ORIGINAL FUNCTION - Keep
def save_text(text, path):
    """
    Save text to a TXT file.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# NEW FUNCTION - Read Pluto PDF
def read_pdf(path):
    """
    Extract text from all pages of a PDF.

    Input:
        path: PDF file path

    Output:
        str: Extracted PDF text
    """

    pages = []

    # Open PDF and close it automatically afterward
    with pymupdf.open(path) as document:

        for page in document:
            # Extract text from each page
            text = page.get_text()

            if isinstance(text, str) and text.strip():
                pages.append(text)

    # Combine all pages into one string
    transcript = "\n".join(pages)

    # Reuse the original cleaning function
    cleaned_transcript = clean_text(transcript)

    if not cleaned_transcript:
        raise ValueError("The PDF contains no extractable text.")

    return cleaned_transcript


# NEW FUNCTION - Prepare user inputs
def prepare_podcast_input(
    birth_date,
    birth_time,
    birth_city,
    personal_question,
    pdf_context
):
    """
    Validate and organize the information for the LLM.

    Output:
        dict containing the PDF context and user information.
    """

    # Check that all required fields have values
    if not all([
        birth_date,
        birth_time,
        birth_city,
        personal_question
    ]):
        raise ValueError("Please complete all fields.")

    # Validate the birth date
    try:
        date = datetime.strptime(
            str(birth_date).strip(), "%Y-%m-%d"
        ).date()
    except ValueError:
        raise ValueError("Birth date must use YYYY-MM-DD.")

    if date > datetime.now().date():
        raise ValueError("Birth date cannot be in the future.")

    # Validate the birth time
    try:
        time = datetime.strptime(
            str(birth_time).strip(), "%H:%M"
        ).time()
    except ValueError:
        raise ValueError("Birth time must use HH:MM.")

    # Remove spaces around text inputs
    birth_city = str(birth_city).strip()
    personal_question = str(personal_question).strip()

    if not birth_city or not personal_question:
        raise ValueError("City and question cannot be empty.")

    if not isinstance(pdf_context, str) or not pdf_context.strip():
        raise ValueError("PDF context must be a non-empty string.")

    # Organize all the information in one dictionary
    podcast_context = {
        "source_context": pdf_context,
        "birth_date": date.isoformat(),
        "birth_time": time.strftime("%H:%M"),
        "birth_city": birth_city,
        "personal_question": personal_question
    }

    return podcast_context


# ORIGINAL TEST - Keep
if __name__ == "__main__":
    text = read_transcript("lesson.txt")
    cleaned = clean_text(text)
    save_text(cleaned, "clean_lesson.txt")
    print("Saved to clean_lesson.txt")