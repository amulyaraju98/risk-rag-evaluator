import os

def read_sop(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            print(file.read())
    else:
        print(f"File not found: {file_path}")

read_sop('data/sops/Merchant Onboarding.md')
