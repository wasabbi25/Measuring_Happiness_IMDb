# How the dataset actually works. 

# The dataset is not one single file. Each file contains one movie review. 
# The filename encodes metadata: [id]_[rating].txt. 
# For example, 200_8.txt means review_id = 200 and rating = 8. 
# The folder in which the file is located tells the sentiment label. 
# pos = positive, neg = negative. 

# What the csv should look like: 

# One row per review. 

# Columns explained: 

# review_id: the id of the review, extracted from the filename.
# rating: star rating (1-10)
# sentiment: pos/neg label
# split: train or test
# text: review content

# Import libraries we need

import os
from zipfile import Path
import pandas as pd

# Get absolute path to this script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define where the raw dataset lives


# This folder contains the original IMDb dataset
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "raw", "imdb")

# Define where we want to save the cleaned dataset
# This will become one single CSV file containing all reviews
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "..", "data", "processed", "imdb_reviews_clean.csv")


# Create an empty list to store rows of data

# Each movie review will become one dictionary

rows = []

# Loop through dataset structure

# The dataset is split into two groups:
# train (25k reviews)
# test (25k reviews)

for split in ["train", "test"]:

    # Inside each split there are folders:
    # pos → positive reviews
    # neg → negative reviews

    for sentiment in ["pos", "neg"]:
        folder = os.path.join(DATA_DIR, split, sentiment) # Build the full folder path

        # Loop through all review files in that folder

        for file in os.listdir(folder):

            # Only process .txt files
            # (ignore hidden files like .DS_Store)

            if not file.endswith(".txt"):
                continue

            # Extract metadata from filename

            review_id, rating = file.replace(".txt", "").split("_")

            # Build full file path
            path = os.path.join(folder, file)

            # Read the review text
            # Open the text file and read its content

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            # Store review data as a dictionary

            rows.append({
                "review_id": int(review_id),   # convert id to integer
                "rating": int(rating),         # convert rating to integer
                "sentiment": sentiment,        # pos or neg
                "split": split,                # train or test
                "text": text                   # full review text
            })

# Convert collected rows into a DataFrame

# pandas DataFrame = table structure similar to Excel

df = pd.DataFrame(rows)

# Tokenize reviews into words
import re
def tokenize_reviews(df, text_column="text"):
    df["tokens"] = df[text_column].apply(lambda x: re.findall(r"\b\w+\b", x))
    return df

df = tokenize_reviews(df)
# Load labMT lexicon
def load_labmt_lexicon(filepath):
    lexicon = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for _ in range(4):
            next(f)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            word = parts[0]
            score = float(parts[2])
            lexicon[word] = score
    return lexicon

# Path to labMT lexicon (relative to script)
LABMT_PATH = os.path.join(SCRIPT_DIR, "..", "..", "PROJECT_1", "data", "raw", "Data_Set.txt")
labmt_lexicon = load_labmt_lexicon(LABMT_PATH)

# Compute happiness score for each review
def compute_happiness_score(tokens, lexicon):
    scores = [lexicon[word] for word in tokens if word in lexicon]
    if scores:
        return sum(scores) / len(scores)
    else:
        return None

df["happiness_score"] = df["tokens"].apply(lambda tokens: compute_happiness_score(tokens, labmt_lexicon))
# Plot histogram of happiness scores (overall)
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
df["happiness_score"].dropna().hist(bins=50)
plt.xlabel("Happiness Score")
plt.ylabel("Number of Reviews")
plt.title("Distribution of Happiness Scores in IMDb Reviews")
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "..", "figures", "happiness_score_histogram.png"))
plt.show()
# Summary statistics for happiness scores

overall_stats = df["happiness_score"].describe()
print("\nOverall happiness score summary:")
print(overall_stats)

for sentiment in ["pos", "neg"]:
    stats = df[df["sentiment"] == sentiment]["happiness_score"].describe()
    print(f"\nHappiness score summary for {sentiment} reviews:")
    print(stats)

# Save summary statistics to tables folder
summary_dict = {
    "overall": overall_stats,
    "pos": df[df["sentiment"] == "pos"]["happiness_score"].describe(),
    "neg": df[df["sentiment"] == "neg"]["happiness_score"].describe()
}
summary_df = pd.DataFrame(summary_dict)
summary_path = os.path.join(SCRIPT_DIR, "..", "tables", "happiness_score_summary_stats.csv")
summary_df.to_csv(summary_path)
print(f"\nSaved summary statistics to: {summary_path}")

# Save labMT lexicon dictionary to CSV
import csv
lexicon_path = os.path.join(SCRIPT_DIR, "..", "tables", "labMT_lexicon.csv")
with open(lexicon_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "happiness_score"])
    for word, score in labmt_lexicon.items():
        writer.writerow([word, score])
print(f"Saved labMT lexicon dictionary to: {lexicon_path}")

# Plot histogram by sentiment
plt.figure(figsize=(8, 5))
for sentiment in ["pos", "neg"]:
    df[df["sentiment"] == sentiment]["happiness_score"].dropna().hist(bins=50, alpha=0.5, label=sentiment)
plt.xlabel("Happiness Score")
plt.ylabel("Number of Reviews")
plt.title("Happiness Scores by Sentiment")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "..", "figures", "happiness_score_by_sentiment.png"))
plt.show()

# Basic text cleaning
# Remove newline characters
# Movie reviews often contain line breaks

df["text"] = df["text"].str.replace("\n", " ")

# Remove extra whitespace at start/end

df["text"] = df["text"].str.strip()

# Convert text to lowercase
# Helps when matching words with the hedonometer lexicon later

df["text"] = df["text"].str.lower()

# Save the cleaned dataset as a CSV file
# This creates one dataset with all reviews

df.to_csv(OUTPUT_FILE, index=False)

# Print confirmation in terminal

print("Saved cleaned dataset to:", OUTPUT_FILE)

# Print number of rows and columns
print("Dataset shape:", df.shape)

# Small sanity check: 

print(df["sentiment"].value_counts())
print(df["rating"].value_counts())

# Expected resulte: pos 2500, neg 2500, ratings from 1 to 10 with varying counts.

# How we will use this for hedonometer? 
# Tokenize each review: review > words
# Match tokens with labMT lexicon 
# Compute: average happiness score per review, then compare things like pos vs neg reviews, train vs test, rating vs happiness score. 

# Sampling
# Imports for sampling 
from pathlib import Path
import random

# Set random seed for reproducibility
random.seed(42)

# Define a function to sample reviews from a specific split and sentiment
def sample_reviews(data_dir, split, sentiment, n):
    """
    Sample n reviews from a specific split (train/test) and sentiment (pos/neg) 
    """
    folder = Path(data_dir) / split / sentiment # Build the folder path using pathlib
    files = list(folder.glob("*.txt")) # Get all .txt files in the specified folder
    return random.sample(files, n) # Sample n files randomly from the list of files in that folder

# Sample 50 positive reviews from train and 50 from test
train_pos = sample_reviews(DATA_DIR, "train", "pos", 50)
test_pos = sample_reviews(DATA_DIR, "test", "pos", 50)

# Sample 50 negative reviews from train and 50 from test
train_neg = sample_reviews(DATA_DIR, "train", "neg", 50)
test_neg = sample_reviews(DATA_DIR, "test", "neg", 50)

# Combine all sampled files
sampled_files = train_pos + test_pos + train_neg + test_neg

# Load into a DataFrame
sample_rows = [] # Initialize an empty list to store the sampled review data as dictionaries
for file_path in sampled_files: # Loop through each sampled file path
    review_id, rating = file_path.stem.split("_") # Extract review_id and rating from filename
    with open(file_path, "r", encoding="utf-8") as f: # Read the review text
        text = f.read().replace("\n", " ").strip().lower() # Text cleaning: remove newlines, strip whitespace, convert to lowercase
    split = "train" if "train" in str(file_path) else "test" # Determine split from file path
    sentiment = "pos" if "pos" in str(file_path) else "neg" # Determine sentiment from file path
    sample_rows.append({ # Store the review data as a dictionary
        "review_id": int(review_id), # Convert review_id to integer
        "rating": int(rating), # Convert rating to integer
        "sentiment": sentiment, # pos or neg
        "split": split, # train or test
        "text": text # Cleaned review text
    }) # Append the dictionary to the list of sample rows

# Create DataFrame
sample_df = pd.DataFrame(sample_rows)

# Sanity check
print(sample_df.head()) # Print the first few rows of the sampled DataFrame to verify the structure and content
print("Total sampled reviews:", len(sample_df)) # Print number of sampled reviews
print(sample_df["sentiment"].value_counts()) # Check the distribution of sentiment labels in the sampled dataset
print(sample_df["split"].value_counts()) # Check the distribution of train/test splits in the sampled dataset

# Save to CSV
SAMPLE_OUTPUT = Path(SCRIPT_DIR) / ".." / "data" / "processed" / "imdb_review_sample_200.csv" # Define the output path for the sampled dataset
sample_df.to_csv(SAMPLE_OUTPUT, index=False) # Save the sampled DataFrame to a CSV file without the index
print(f"Saved sample to: {SAMPLE_OUTPUT}") # Print where the sampled dataset was saved