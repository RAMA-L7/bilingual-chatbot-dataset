import os
import json

WEATHER_DIR = "data/weather"

def normalize_format_2_to_format_1(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        converted = []
        for entry in data:
            if "turns" in entry:
                new_entry = {
                    "id": entry["id"],
                    "language": entry.get("language", "bilingual"),
                    "conversation": entry["turns"]
                }
                converted.append(new_entry)
            else:
                print(f"⚠️ Skipped (no 'turns'): {entry.get('id')}")
        with open(file_path, "w", encoding="utf-8") as f_out:
            json.dump(converted, f_out, indent=2, ensure_ascii=False)
        print(f"✅ Normalized: {file_path}")
    else:
        print(f"❌ Not a list format: {file_path}")

# Run for all .json files in weather/
for file in os.listdir(WEATHER_DIR):
    if file.endswith(".json"):
        normalize_format_2_to_format_1(os.path.join(WEATHER_DIR, file))
