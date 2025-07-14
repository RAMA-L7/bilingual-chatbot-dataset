import os
import json

def fix_list_format(file_path, file_id=None, lang="bilingual"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Only fix files that start with a list (invalid)
        if isinstance(data, list):
            new_data = {
                "id": file_id or os.path.splitext(os.path.basename(file_path))[0],
                "language": lang,
                "conversation": data
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Fixed: {file_path}")
        else:
            print(f"✔️ Already valid: {file_path}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

# 🚀 Start fixing all files in the /data directory
def fix_all_jsons():
    root_dir = "data"
    for domain_folder in os.listdir(root_dir):
        full_domain_path = os.path.join(root_dir, domain_folder)
        if os.path.isdir(full_domain_path):
            for filename in os.listdir(full_domain_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(full_domain_path, filename)
                    fix_list_format(file_path)

if __name__ == "__main__":
    fix_all_jsons()
