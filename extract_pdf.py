import pymupdf  # Library for reading PDF files

# Input PDF and output text file
pdf_path = "Pattern-App text .pdf"
txt_path = "transcript.txt"

# Open the PDF
document = pymupdf.open(pdf_path)

# Extract text from every page
pages = []

for page in document:
    text = page.get_text()
    pages.append(text)

document.close()

# Combine all pages into one text string
transcript = "\n".join(pages)

# Save extracted text to a .txt file
with open(txt_path, "w", encoding="utf-8") as file:
    file.write(transcript)

print(f"Extracted {len(pages)} pages into {txt_path}")
print(f"Word count: {len(transcript.split())}")