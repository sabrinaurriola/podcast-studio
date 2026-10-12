def read_transcript(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def clean_text(text):
    return " ".join(text.split())

if __name__ == "__main__":
    text = read_transcript("lesson.txt")
    print(clean_text(text))