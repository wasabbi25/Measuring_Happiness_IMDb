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
import pandas as pd

# Define where the raw dataset lives

# This folder contains the original IMDb dataset

DATA_DIR = "../data/raw/imdb"

# Define where we want to save the cleaned dataset
# This will become one single CSV file containing all reviews

OUTPUT_FILE = "../data/processed/imdb_reviews_clean.csv"


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