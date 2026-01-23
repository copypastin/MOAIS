import os
import random
from src.utils.HashManager import HashManager

# Get all hashes as a dictionary {filename: hashes}
all_hashes = HashManager.compute_directory_hashes(os.path.join(os.path.dirname(__file__), "output"))

# Pick a random file as target
filenames = list(all_hashes.keys())
target_filename = random.choice(filenames)
target_hashes = all_hashes[target_filename]

print(f"Target file: {target_filename}\n")

# Compare with all other files
for filename, hashes in all_hashes.items():
    if filename != target_filename:
        similarity = HashManager.compute_similarity_hashes(target_hashes, hashes)
        print(f"{filename}: Similarity = {similarity}")