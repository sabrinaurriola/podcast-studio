def read_transcript(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def clean_text(text):
    return " ".join(text.split())

def save_text(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    text = read_transcript("lesson.txt")
    cleaned = clean_text(text)
    save_text(cleaned, "clean_lesson.txt")
    print("Saved to clean_lesson.txt")