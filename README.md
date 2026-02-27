

# Project title + 2-3 sentence ove
    The happiness rank shows how happy a word is rated, but the data set also shows how common the word appears in different sources. For example, a word might be very happy (high happiness rank) but not very common in Twitter or song lyrics (low or missing corpus rank). B analysing the labMT 1.0 dataset, our goal is to understand which words are commonly associated as positive or negative across different texts, but also compare how common they are. 

## Dataset section

### Summary Statistics for Happiness Average
They were computer in the src/01_load_and_clean.py 
Here are computed summary statistics for the happiness_average column:
- Mean: 5.38
- Median: 5.44
- Standard deviation: 1.08
- 5th percentile: 3.18
- 95th percentile: 7.08
These numbers help us understand the overall distribution of happiness scores in the dataset. 

- Where it came from: labMT 1.0 dataset (Hedonometer paper)
- What each column means (data dictionary):
	- We made a data dictionary to help us understand what each column in the dataset represents, what type of data it is, and how many missing values there are. This is useful because it makes the dataset less intimidating and helps us know what to look for when analyzing or plotting data. 
	- Here’s a summary of the column names with float and integer:
		- **word**: The word being rated (text, no missing values)
		- **happiness_rank**: Rank of the word by happiness score (integer, no missing values)
		- **happiness_average**: Average happiness score for the word (float, no missing values)
		- **happiness_standard_deviation**: Standard deviation of happiness scores (float, no missing values)
		- **twitter_rank**: Rank in Twitter corpus (float, 5222 missing values)
		- **google_rank**: Rank in Google corpus (float, 5222 missing values)
		- **nyt_rank**: Rank in New York Times corpus (float, 5222 missing values)
		- **lyrics_rank**: Rank in song lyrics corpus (float, 5222 missing values)
	- If a rank is missing, it means the word was not in the top 5,000 for that corpus meaning it is not commonly appearing in the source.


### Sanity Check: Duplicated Words
We checked the dataset for any duplicated words (words that appear more than once). This is important because duplicates could mess up our analysis or make results confusing. Our check found that there are no duplicated words in the dataset, so each word only appears once! This gives us confidence that the data is clean and ready for analysis! Most positive words are: laughter, happiness, love, happy, laughed, laugh, laughing, excellent, laughs, and joy. Most negative words are: terrorist, suicide, rape, terrorism, murder, death, cancer, died, kill, and killed. These do make sense on average for the English understanding that associates are respected. "Makes sense" here would mean likely what you would expect associated with the word positively or negatively. 

### Why take a random sample?
	- We took a random sample of 15 rows from the dataset to get a snapshot of the kind of data we’re working with. It lets us see some real examples. It also helps check for any obvious issues, like weird values or repeated words.
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
5. Dataset Shape
	- The cleaned dataset has 10,222 rows and 8 columns.
6. Missing Ranks
	- If a rank is missing (NaN), it means the word was not in the top 5,000 for that corpus.

## Methods section (what you did in python)

## Results section
- Plots + captions
### Histogram Interpretation
The histogram of happiness_average scatter plot under the figures folder shows the happiness score is out of 10 along the bottom (where 10 is the happiest). The frequency is out of the total number of words in your dataset. At first glance, the scatter plot looks like a bird in flight with wings on either side where words are shown least on each side and the body of the bird is most rounded and clustered. SURPRISINGLY, the distribution is slightly skewed toward positive values around the 6 score being that average people are feeling a 6 in happiness scale. It could also mean there are more happy words than sad ones. There are rarely word with extremely low happiness scores between 1 or 2 which suggests this particular random selection has been generally happy.


### Where to Find Plots and Tables
You can find the generated plots and summary tables in the following folders:

- **figures/**
	- happiness_average_hist.png: Histogram of happiness scores
	- happiness_vs_std_scatter.png: Scatterplot of happiness vs standard deviation
	- twitter_rank_vs_nyt_rank_scatter.png: Comparison of Twitter and NYT ranks
	- corpus_rank_coverage_bar.png: Coverage of ranks across corpora

- **tables/**
	- data_dictionary.csv: Data dictionary for the dataset
	- preview_first_50_rows.csv: Preview of the first 50 rows
	- random_sample_15_rows.csv: Random sample of 15 words
	- top_10_positive_words.csv: Most positive words
	- top_10_negative_words.csv: Most negative words
	- top_15_contested_words.csv: Words with highest disagreement
	- happiness_average_summary_stats.csv: Summary statistics for happiness scores
	- pairwise_overlap_counts.csv: Overlap counts between corpora
	- corpus_rank_coverage.csv: Rank coverage across corpora
	- corpus_overlap_patterns.csv: Patterns of overlap between corpora
	- twitter_common_nyt_missing_top20.csv: Words common in Twitter but missing in NYT
	- word_exhibit_demo_20_words.csv: Demo exhibit of 20 words

These files help you explore and understand the dataset and analysis results.

## Qualitative "exhibit" of words

## Critical reflection

## How to run your code
- Setup steps
- Which scripts to run

## Credits
- Who did what (team roles)
- Citation for the paper / dataset
