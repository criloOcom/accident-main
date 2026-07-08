import time
import re

# Mocking data to simulate the loop
md_content_template = """=== PIECE: Some piece info
Some text goes here.
--- PAGE 1 ---
More text on page 1.
--- PAGE 2 ---
Even more text on page 2.
"""

# Number of iterations to simulate large dataset
num_iterations = 100000

# 1. Baseline: Regex compilation inside the loop
start_time = time.time()
for _ in range(num_iterations):
    md_content = md_content_template
    md_content = re.sub(r'^=== PIECE:.*?\n', '', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^--- PAGE (\d+) ---\n?', r'\n\n--- Page \1 ---\n\n', md_content, flags=re.MULTILINE)
baseline_time = time.time() - start_time
print(f"Baseline (compilation inside loop): {baseline_time:.4f} seconds")

# 2. Optimized: Pre-compiled regex outside the loop
start_time = time.time()
piece_marker_re = re.compile(r'^=== PIECE:.*?\n', flags=re.MULTILINE)
page_marker_re = re.compile(r'^--- PAGE (\d+) ---\n?', flags=re.MULTILINE)

for _ in range(num_iterations):
    md_content = md_content_template
    md_content = piece_marker_re.sub('', md_content)
    md_content = page_marker_re.sub(r'\n\n--- Page \1 ---\n\n', md_content)
optimized_time = time.time() - start_time
print(f"Optimized (compilation outside loop): {optimized_time:.4f} seconds")

print(f"Improvement: {(baseline_time - optimized_time) / baseline_time * 100:.2f}%")
