import json

with open("/tmp/abc_values.json") as f:
    abc_values = json.load(f)

# Split into 3 batches of rows for A2:C50, A51:C100, A101:C138
b1 = abc_values[1:49] # rows 2 to 49
b2 = abc_values[49:99] # rows 50 to 99
b3 = abc_values[99:] # rows 100 to 138

with open("/tmp/abc_b1.json", "w") as f: json.dump(b1, f)
with open("/tmp/abc_b2.json", "w") as f: json.dump(b2, f)
with open("/tmp/abc_b3.json", "w") as f: json.dump(b3, f)
print(f"Batch sizes: {len(b1)}, {len(b2)}, {len(b3)}")
