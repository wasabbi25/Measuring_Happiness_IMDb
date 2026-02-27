
import pandas as pd
import numpy as np

# Step 1. Defining the file paths

raw_path = "data/raw/Data_Set_S1.txt"
clean_path = "data/clean/clean_data.csv"

# Step 2. Loading in the dataset

# The dataset contains some metadata lines at the top. 
# To skip interpreting them, we tell pandas to ignore lines that don't use a tab structure.

df = pd.read_csv(
    raw_path,
    sep="\t",
    skiprows=3,  # Skip the first 3 metadata lines
    skip_blank_lines=True,
    na_values="--"
)

# Step 3. Converting strings into numeric values. 
# Making sure that columns such as ranks, averages, and standard deviations, are actually stored as numeric values in pandas and not as strings. 

numeric_columns = [
    "happiness_rank",
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_rank",
    "nyt_rank",
    "lyrics_rank"
]

# To apply the same operation to each column automatically, instead of repeating code, we stored them in a list. 
# This allows us to use a loop. 

for col in numeric_columns:  # Loop through each column name listed above.
    df[col] = pd.to_numeric( 
        df[col],             # Take the column from the dataframe.
        errors="coerce"      # If a value cannot be converted to a number (like "--"), pandas will replace it with a missing value. 
    )

# pd.to_numeric() attempts to convert the column from text to numeric type (int/float). 
# This is necessary because when pandas loads a file, it sometimes treats numbers as strings, especially if missing values are present, 

# Step 4. Save cleaned DataFrame
df.to_csv(clean_path, index=False)

# Step 5. Sanity check for duplicated words

num_duplicates = df['word'].duplicated().sum()
if num_duplicates == 0:
    print('Sanity check: No duplicated words found in the dataset.')
else:
    print(f'Sanity check: Found {num_duplicates} duplicated words in the dataset.')

# Step 6. Plot histogram of happiness_average
import matplotlib.pyplot as plt

# Step 6. Plot histogram of happiness_average
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 5))
plt.hist(df['happiness_average'], bins=30, color='skyblue', edgecolor='black')
plt.title('Histogram of Happiness Average')
plt.xlabel('Happiness Average')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('figures/happiness_average_hist.png')
plt.close()

# Step 7. Compute summary statistics
mean = df['happiness_average'].mean()
median = df['happiness_average'].median()
std = df['happiness_average'].std()
p5 = df['happiness_average'].quantile(0.05)
p95 = df['happiness_average'].quantile(0.95)
print(f"Mean: {mean:.2f}, Median: {median:.2f}, Std: {std:.2f}, 5th percentile: {p5:.2f}, 95th percentile: {p95:.2f}")

# Step 8. Plot happiness_average vs happiness_standard_deviation scatterplot
plt.figure(figsize=(8, 5))
plt.scatter(df['happiness_average'], df['happiness_standard_deviation'], alpha=0.5)
plt.title('Happiness Average vs Standard Deviation')
plt.xlabel('Happiness Average')
plt.ylabel('Happiness Standard Deviation')
plt.tight_layout()
plt.savefig('figures/happiness_vs_std_scatter.png')
plt.close()

# Step 9. Identify 15 most contested words (highest std)
contested = df.nlargest(15, 'happiness_standard_deviation')[['word', 'happiness_standard_deviation', 'happiness_average']]
contested.to_csv('tables/top_15_contested_words.csv', index=False)
print('Top 15 contested words saved to tables/top_15_contested_words.csv')