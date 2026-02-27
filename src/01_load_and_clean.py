
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
# Making sure that columns that columns such as ranks, averages, and standard deviations, are actually stored as numeric values in mandas and not as strings. 

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
    print(f'Sanity check: {num_duplicates} duplicated words found in the dataset.')