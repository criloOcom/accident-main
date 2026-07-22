import json

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

print(json.dumps({"content": read_file(".dev/app/fix_lois_structure.py")}))
