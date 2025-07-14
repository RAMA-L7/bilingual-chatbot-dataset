import os
import json
from jsonschema import validate, ValidationError

# Schema paths
FORMAT1_SCHEMA = "schema_format1.json"
FORMAT2_SCHEMA = "schema_format2.json"

def load_schema(schema_file):
    with open(schema_file, "r", encoding="utf-8") as f:
        return json.load(f)

schema_format1 = load_schema(FORMAT1_SCHEMA)
schema_format2 = load_schema(FORMAT2_SCHEMA)

def detect_format(data):
    """Detects the JSON format based on keys inside 'conversation' list."""
    if not isinstance(data, dict):
        return None
    conversation = data.get("conversation")
    if not isinstance(conversation, list):
        return None

    if all("user" in turn and "bot" in turn for turn in conversation):
        return schema_format1
    elif all("speaker" in turn and "en" in turn and "te" in turn for turn in conversation):
        return schema_format2
    else:
        return None

def validate_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # ✅ Accept top-level list as valid (Format 1)
        if isinstance(data, list):
            if all(isinstance(entry, dict) and "conversation" in entry for entry in data):
                return f"✅ Valid Format 1: {file_path}"

        # ✅ Accept alternate format if needed (Format 2)
        if isinstance(data, dict) and "conversation" in data:
            conversation = data["conversation"]
            if isinstance(conversation, list) and all("conversation" in turn for turn in conversation):
                return f"✅ Valid Format 2: {file_path}"

        return f"❌ Could not detect known format in {file_path}"

    except Exception as e:
        return f"❌ Error in {file_path}: {e}"


def validate_all_jsons(root_dir="data"):
    results = []
    for domain in os.listdir(root_dir):
        domain_path = os.path.join(root_dir, domain)
        if os.path.isdir(domain_path):
            for file in os.listdir(domain_path):
                if file.endswith(".json"):
                    file_path = os.path.join(domain_path, file)
                    results.append(validate_json_file(file_path))
    return results

if __name__ == "__main__":
    results = validate_all_jsons()
    for res in results:
        print(res)
