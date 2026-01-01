import os

SOPS_DIR = "data/sops"

def read_sop(file_path):
    """Print the content of a single SOP file."""
    if os.path.exists(file_path):
        print("=" * 80)
        print(f"READING: {file_path}")
        print("=" * 80)
        with open(file_path, "r") as f:
            print(f.read())
        print("\n\n")
    else:
        print(f"File not found: {file_path}")

def read_all_sops():
    """Loop through all files in data/sops and read them."""
    if not os.path.isdir(SOPS_DIR):
        print(f"SOPs folder not found: {SOPS_DIR}")
        return

    files = sorted(os.listdir(SOPS_DIR))
    if not files:
        print(f"No SOP files found in {SOPS_DIR}")
        return

    for name in files:
        if name == ".DS_Store":
            continue
        file_path = os.path.join(SOPS_DIR, name)
        read_sop(file_path)

if __name__ == "__main__":
    read_all_sops()
