import json

def load_subject_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text
    except FileNotFoundError:
        return "Subject text not found."

def save_progress(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_progress(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}