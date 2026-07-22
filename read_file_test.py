with open(".dev/app/fix_lois_structure.py", "r") as f:
    lines = f.readlines()
    for i in range(0, len(lines), 50):
        print("".join(lines[i:i+50]))
        print("--- chunk ---")
