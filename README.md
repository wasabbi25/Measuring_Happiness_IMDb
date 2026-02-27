

# Project title + 2-3 sentence overview

## Dataset section

- Where it came from: labMT 1.0 dataset (Hedonometer paper)
- What each column means (data dictionary):
	- We made a data dictionary to help us understand what each column in the dataset represents, what type of data it is, and how many missing values there are. This is useful for beginners because it makes the dataset less intimidating and helps us know what to look for when analyzing or plotting data.
	- Here’s a summary of the columns:
		- **word**: The word being rated (text, no missing values)
		- **happiness_rank**: Rank of the word by happiness score (integer, no missing values)
		- **happiness_average**: Average happiness score for the word (float, no missing values)
		- **happiness_standard_deviation**: Standard deviation of happiness scores (float, no missing values)
		- **twitter_rank**: Rank in Twitter corpus (float, 5222 missing values)
		- **google_rank**: Rank in Google corpus (float, 5222 missing values)
		- **nyt_rank**: Rank in New York Times corpus (float, 5222 missing values)
		- **lyrics_rank**: Rank in song lyrics corpus (float, 5222 missing values)
	- If a rank is missing, it means the word was not in the top 5,000 for that corpus.

### Why take a random sample?
	- We took a random sample of 15 rows from the dataset to get a quick look at the kind of data we’re working with. This is helpful for beginners because it lets us see some real examples without having to scroll through thousands of rows. It also helps check for any obvious issues, like weird values or repeated words.
	- The random sample is saved in `tables/random_sample_15_rows.csv`.

### Data Cleaning Steps
1. Load the Dataset
	- Read the tab-delimited file into a pandas DataFrame.
	- Skip the first 3 metadata lines at the top of the file.
	- Replace '--' with missing values.
	- Convert numeric columns to proper types (float/int).
	- Confirm the number of rows and columns.
2. Save the Cleaned Data
	- The cleaned DataFrame is saved as `data/clean/clean_data.csv`.
3. What does it mean to clean the data file?
	- Cleaning the data means:
	  - Removing or handling metadata and comment lines.
	  - Ensuring all numeric columns are stored as numbers, not text.
	  - Replacing placeholder values (like '--') with proper missing value markers.
	  - Making the dataset ready for analysis by fixing types and structure.
```python
import pandas as pd
raw_path = "data/raw/Data_Set_S1.txt"
clean_path = "data/clean/clean_data.csv"
df = pd.read_csv(
	 raw_path,
	 sep="\t",
	 skiprows=3,
	 skip_blank_lines=True,
	 na_values="--"
)
numeric_columns = [
	 "happiness_rank", "happiness_average", "happiness_standard_deviation",
	 "twitter_rank", "google_rank", "nyt_rank", "lyrics_rank"
]
for col in numeric_columns:
	 df[col] = pd.to_numeric(df[col], errors="coerce")
df.to_csv(clean_path, index=False)
```
5. Dataset Shape
	- The cleaned dataset has 10,222 rows and 8 columns.
6. Missing Ranks
	- If a rank is missing (NaN), it means the word was not in the top 5,000 for that corpus.

## Methods section (what you did in python)

## Results section
- Plots + captions
- Interpretation in plain language

## Qualitative "exhibit" of words

## Critical reflection

## How to run your code
- Setup steps
- Which scripts to run

## Credits
- Who did what (team roles)
- Citation for the paper / dataset
