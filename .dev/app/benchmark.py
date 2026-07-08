import time
from extract_legal_refs import extract_legal_refs

# Create a dummy large text
text = "Voici un texte très long avec quelques références légales comme l'article 1240 du code civil et l'art. 145 du CPC. " * 10000

start_time = time.time()
for _ in range(10):
    extract_legal_refs(text)
end_time = time.time()

print(f"Time taken: {end_time - start_time:.4f} seconds")
