import os
from textwrap import wrap

SOPS_DIR = "data/sops"


def read_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r") as f:
        return f.read()


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 100):
  
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap  

    return chunks


def chunk_by_section(text):
    sections = text.split("## ")
    return [section.strip() for section in sections if section.strip()]


def chunk_all_sops():
    files = sorted(os.listdir(SOPS_DIR))
    files = [f for f in files if f != ".DS_Store"]

    if not files:
        print(f"No SOP files found in {SOPS_DIR}")
        return

    for name in files:
        path = os.path.join(SOPS_DIR, name)
        text = read_file(path)
        chunks = chunk_text(text, chunk_size=400, overlap=80)

        print("=" * 80)
        print(f"FILE: {name}")
        print(f"Total characters: {len(text)}")
        print(f"Total chunks: {len(chunks)}")
        print("-" * 80)

        for i, chunk in enumerate(chunks, start=1):
            print(f"\n--- CHUNK {i}/{len(chunks)} ---")
            print(chunk)
        print("\n\n")


if __name__ == "__main__":
    chunk_all_sops()
