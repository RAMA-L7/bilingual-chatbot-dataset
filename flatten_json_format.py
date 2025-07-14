import os
import json

def flatten_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Fix if current file has a nested format
        if isinstance(data, dict) and "conversation" in data:
            inner_list = data["conversation"]
            if isinstance(inner_list, list) and all("conversation" in item for item in inner_list):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(inner_list, f, indent=2, ensure_ascii=False)
                print(f"✅ Flattened: {file_path}")
            else:
                print(f"⚠️ Not flattenable: {file_path}")
        else:
            print(f"✔️ Already valid: {file_path}")

    except Exception as e:
        print(f"❌ Error in {file_path}: {e}")

def run_flattener():
    root = "data"
    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    flatten_json_file(os.path.join(folder_path, file))

if __name__ == "__main__":
    run_flattener()
