from src.data_processor import read_pdf, prepare_podcast_input
from src.llm_processor import create_script


# STEP 1: Extract the PDF context
pdf_context = read_pdf("Pattern-App text .pdf")


# STEP 2: Simulate information entered through Gradio
podcast_context = prepare_podcast_input(
    birth_date="1995-06-15",
    birth_time="14:30",
    birth_city="Madrid, Spain",
    personal_question=(
        "Why do I struggle to let go of control "
        "when my life changes?"
    ),
    pdf_context=pdf_context
)


# STEP 3: Generate the personalized podcast script
script = create_script(podcast_context)


# STEP 4: Display the result
print(script)

print("\n--- TEST RESULTS ---")
print("Word count:", len(script.split()))
print("Contains HOST_A:", "HOST_A:" in script)
print("Contains HOST_B:", "HOST_B:" in script)