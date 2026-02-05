import os
import random
from src.utils.HashManager import HashManager
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# Get all hashes as a dictionary {filename: hashes}
all_hashes = HashManager.compute_directory_hashes(os.path.join(os.path.dirname(__file__), "output"))

target_file = os.path.join(os.path.dirname(__file__), "my_work.cpp")
target_hashes = HashManager.compute_file_hashes(target_file)


# Compare with all other files
for filename, hashes in all_hashes.items():
    similarity = HashManager.compute_similarity_hashes(target_hashes, hashes)
    print(f"{filename}: Similarity = {similarity}")

