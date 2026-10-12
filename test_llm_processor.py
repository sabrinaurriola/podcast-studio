# Import the function we want to test
from src.llm_processor import create_script

# Read the extracted transcript
with open("transcript.txt", "r", encoding="utf-8") as file:
    transcript = file.read()

# Generate the podcast script
script = create_script(transcript)

# Display the result
print(script)
print("\nWord count:", len(script.split()))
