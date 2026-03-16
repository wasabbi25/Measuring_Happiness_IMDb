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
import re
import csv
import random
import matplotlib.pyplot as plt
import numpy as np

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

# Convert collected rows into a pandas DataFrame (table structure similar to Excel)
df = pd.DataFrame(rows)

# Basic text cleaning 
# Remove newline characters
df["text"] = df["text"].str.replace("\n", " ")
# Remove extra whitespace at start/end
df["text"] = df["text"].str.strip()
# Convert text to lowercase (helps matching with lexicon)
df["text"] = df["text"].str.lower()

# Tokenize reviews into words
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

# Expected results: pos 2500, neg 2500, ratings from 1 to 10 with varying counts.

# Plot histogram of happiness scores (overall)
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

# How we will use this for hedonometer? 
# Tokenize each review: review > words
# Match tokens with labMT lexicon 
# Compute: average happiness score per review, then compare things like pos vs neg reviews, train vs test, rating vs happiness score. 

# Sampling 
# Set random seed for reproducibility
random.seed(42)

# Function to sample n reviews from a given split and sentiment
def sample_from_df(df, split, sentiment, n):
    subset = df[(df["split"] == split) & (df["sentiment"] == sentiment)]
    return subset.sample(n=n, random_state=42)

# Sample 50 positive reviews from train and 50 from test
train_pos = sample_from_df(df, "train", "pos", 50)
test_pos = sample_from_df(df, "test", "pos", 50)

# Sample 50 negative reviews from train and 50 from test
train_neg = sample_from_df(df, "train", "neg", 50)
test_neg = sample_from_df(df, "test", "neg", 50)

# Combine all samples into one DataFrame
sample_df = pd.concat([train_pos, test_pos, train_neg, test_neg]).reset_index(drop=True)

# Sanity check 
print(sample_df.head()) # Check the first few rows of the sample to ensure it looks correct
print("Total sampled reviews:", len(sample_df)) #for count of sampled reviews : should be 200
print(sample_df["sentiment"].value_counts()) #for count by sentiment : should be 100 pos and 100 neg 
print(sample_df["split"].value_counts()) #for count by split : should be 100 train and 100 test

# Save sample to CSV
SAMPLE_OUTPUT = os.path.join(SCRIPT_DIR, "..", "data", "processed", "imdb_review_sample_200.csv")
sample_df.to_csv(SAMPLE_OUTPUT, index=False)
print(f"Saved sample to: {SAMPLE_OUTPUT}")

# Distribution checks for comparing sample vs full dataset 

# Statistics
# Overall happiness score statistics for sample 
sample_overall_stats = sample_df["happiness_score"].describe()
print("\nOverall happiness score summary for sample:")
print(sample_overall_stats)
# Happiness score by sentiment stats for sample 
sample_sentiment_stats = sample_df.groupby("sentiment")["happiness_score"].describe()
print("\nHappiness score by sentiment for sample:")
print(sample_sentiment_stats)
# Save sample statistics to CSV
sample_summary_dict = {
    "sample_overall": sample_df["happiness_score"].describe(),
    "sample_pos": sample_df[sample_df["sentiment"] == "pos"]["happiness_score"].describe(),
    "sample_neg": sample_df[sample_df["sentiment"] == "neg"]["happiness_score"].describe()
}
sample_summary_df = pd.DataFrame(sample_summary_dict)
sample_summary_path = os.path.join(SCRIPT_DIR, "..", "tables", "sample_happiness_summary_stats.csv")
sample_summary_df.to_csv(sample_summary_path)
print(f"\nSaved sample summary statistics to: {sample_summary_path}")

# Histograms
# Plot histogram of happiness scores for the sample
plt.figure(figsize=(8, 5))
sample_df["happiness_score"].hist(bins=20)
plt.title("Sample Happiness Scores")
plt.xlabel("Happiness Score")
plt.ylabel("Number of Reviews")
plt.savefig(os.path.join(SCRIPT_DIR, "..", "figures", "sample_happiness_score_histogram.png"))
plt.show()

# Plot histogram of happiness scores by sentiment for the sample
plt.figure(figsize=(8, 5))
for sentiment in ["pos", "neg"]:
    sample_df[sample_df["sentiment"] == sentiment]["happiness_score"].hist(bins=20, alpha=0.5, label=sentiment)
plt.title("Sample Happiness Scores by Sentiment")
plt.xlabel("Happiness Score")
plt.ylabel("Number of Reviews")
plt.legend()
plt.savefig(os.path.join(SCRIPT_DIR, "..", "figures", "sample_happiness_score_by_sentiment.png"))
plt.show()

# Baseline point estimate

# Compute average happiness score for positive reviews in the sample
sample_pos_mean = sample_df[sample_df["sentiment"] == "pos"]["happiness_score"].mean()
print(f"Average happiness score for positive reviews in sample: {sample_pos_mean:.2f}")

# Compute average happiness score for negative reviews in the sample
sample_neg_mean = sample_df[sample_df["sentiment"] == "neg"]["happiness_score"].mean()
print(f"Average happiness score for negative reviews in sample: {sample_neg_mean:.2f}")

# Difference
score_diff = sample_pos_mean - sample_neg_mean
print(f"Difference in average happiness score (pos - neg): {score_diff:.2f}")

# Quantifying uncertainty 

# Separate the positive and negative reviews in the sample
pos_reviews = sample_df[sample_df["sentiment"] == "pos"]["happiness_score"].dropna().values
neg_reviews = sample_df[sample_df["sentiment"] == "neg"]["happiness_score"].dropna().values

# Define the bootstrap function
def bootstrap_mean(data, n_bootstrap=1000, seed=42):
    np.random.seed(seed)
    bootstrap_means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_means.append(np.mean(sample))
    return np.array(bootstrap_means)

# Compute bootstrap distributions for positive and negative reviews
pos_bootstrap_means = bootstrap_mean(pos_reviews, n_bootstrap= 1000)
neg_bootstrap_means = bootstrap_mean(neg_reviews, n_bootstrap=1000)

# 95% confidence intervals for each group
pos_lower = np.percentile(pos_bootstrap_means, 2.5)
pos_upper = np.percentile(pos_bootstrap_means, 97.5)
print(f"95% confidence interval for positive reviews: [{pos_lower:.2f}, {pos_upper:.2f}]")

neg_lower = np.percentile(neg_bootstrap_means, 2.5)
neg_upper = np.percentile(neg_bootstrap_means, 97.5)
print(f"95% confidence interval for negative reviews: [{neg_lower:.2f}, {neg_upper:.2f}]")

# Bootstrap the difference
bootstrap_diff = pos_bootstrap_means - neg_bootstrap_means

# Compute 95% confidence interval for the difference
lower_bound = np.percentile(bootstrap_diff, 2.5)
upper_bound = np.percentile(bootstrap_diff, 97.5)
print(f"95% confidence interval for the difference in means (pos - neg): [{lower_bound:.2f}, {upper_bound:.2f}]")
