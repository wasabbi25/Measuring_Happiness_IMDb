

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
### Histogram Interpretation
The histogram of happiness_average scatter plot under the figures folder shows the happiness score is out of 10 along the bottom (where 10 is the happiest). The frequency is out of the total number of words in your dataset. At first glance, the scatter plot looks like a bird in flight with wings on either side where words are shown least on each side and the body of the bird is most rounded and clustered. SURPRISINGLY, the distribution is slightly skewed toward positive values around the 6 score being that average people are feeling a 6 in happiness scale. It could also mean there are more happy words than sad ones. There are rarely word with extremely low happiness scores between 1 or 2 which suggests this particular random selection has been generally happy.
### Where to Find Plots and Tables
Plots and summary tables are in the following folders:

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


## Qualitative "exhibit" of words

## Critical reflection

### Data Provenance: How Was This Dataset Generated?
The labMT 1.0 dataset was built through the following pipeline:

- **World Selection:** Words are selected from 4 large text corpora,(Twitter, Google Books, New York Times, various song lyrics) and taking up the top 5,000 most frequent words from each source. A final set of 10,222 words were made after removing duplicates.

- **Annotation Production:** Each word was sent to Amazon Mechanical Turk (MTurk), a crowdsourcing platform where paid online workers complete small tasks.

- **Rating Task**: Workers rated each word on a scale from 1 (saddest) to 9 (happiest), seeing only the word with no context.

- **Sample Size**: Each word was rated by 50 different workers.

5. **Score Computation**: The 50 ratings were averaged to produce 'happiness_average'; the spread of disagreement was captured as 'happiness_standard_deviation'.


### Consequences and Limitations
Below we identify five consequential design choices in the labMT dataset, along with what each makes easier or harder to see, supported by concrete examples from our exploration.

- **Words are rated without context:**
	- Annotators saw only a single word (no sentence, no surrounding text)
	- Consequence: Words with multiple meanings or strong slang usage cannot be scored accurately (Dataset cannot distinguish between a word used ironically or affectionately)
	- Example: 'Fucking' has the highest standard deviation in the entire dataset (sd = 2.93) and a middling average score of 4.64. Some raters likely treated it as a profanity (low happiness), while others associate it with emphasis or casual speech (neutral or higher). 
	- Conclusion: Without context, these readings collapse into a single ambiguous number.

- **Annotators are a self selected online population:**
	- MTurk workers (tend to be younger, English speaking, and based in the US or India) are served as sole judges of word happiness.
	- Consequence: The scores reflect the cultural intuitions of a narrow demographic, not humanity broad. Words associated with specific communities, religions, subcultures may be systematically over, or under rated.
	- Example: 'Churches' has a mean happiness score of 5.70 but a standard deviation of 2.46, one of the highest in the dataset. 
	- Conclusion: This high disagreement reflects the annotator pool's varied relationships with religion, a pattern that would look very different with a more globally diverse sample.

- **The dataset was collected in 2009–2011:**
	- Word frequency and sentiment ratings were gathered over a fixed historical window
	- Consequence: Language evolves: Words gain new meanings, enter or exit mainstream use, and shift in emotional valence over time and captures it. 
	- Example: 'Capitalism' scores 5.16 with a standard deviation of 2.45. 
	- Conclusion: Given major economic and political shifts since 2011, the same word rated today would likely produce a very different and possibly more polarized distribution.

- **Only English words are included**
	- The word list was drawn from English language (non-English words were excluded.)
	- Consequence: In particular, Twitter is a multilingual platform. Filtering for English erases the emotional language of non-English speakers and multilingual communities.
	- Example: 'que' (a common Spanish word) appears at Twitter rank 194, meaning it is genuinely frequent in the Twitter corpus, yet it is excluded from the NYT corpus. 
	- Conclusion: Including it in the word list without Spanish-speaking annotators means its happiness score is shaped by English speakers who may treat it as a foreign or meaningless word.

- **Twitter slang is structurally absent from formal corpora**
	- Corpus rank columns reflect four very different text sources, but no adjustment is made for the fact that each corpus has its own vocabulary norms.
	- Consequence: Words that are extremely common in informal digital communication are treated as rare, because they do not appear in formal writing, even when they carry strong emotional meaning for millions of users.
	- Example: 'rt' (retweet), 'lol', 'haha' are all in Twitter's top 200 most frequent words, yet they are entirely absent from the NYT corpus. Our analysis found 952 words that appear only in Twitter and nowhere else. T
	- Conclusion: Many of theses emotionally expressive informal words are effectively invisible to any analysis that relies on corpus overlap.

### If we were to use this dataset as an instrument today... (Instrument Note)

- What would we trust this dataset to measure well?:

	The labMT dataset is well suited for capturing the average emotional valence of common English words, as perceived by a general online English speaking population circa 2009–2011. 
	
	It is reliable for broad, aggregate comparisons (confirming that words like 'laughter' and 'love' are widely perceived as positive, or that words like 'murder' and 'suicide' score low across most annotators.) 
	
	The large sample size (50 raters per word) and the consistency of clearly positive or negative words suggest the instrument is powerfully built for the emotional extremes of the word list.

- What would we refuse to claim based on it?:

	We would not claim that this dataset measures universal human happiness, nor that it captures how any specific community (defined by language, culture, age, or historical moment) actually feels about words. 
	
	The contested words in our analysis ('fucking' sd = 2.93, 'capitalism' sd = 2.45, 'churches' sd = 2.46) make visible that average happiness can obscure deep disagreement.
	
	A single number cannot represent polarized reactions. We would also resist applying this dataset to contemporary social media language, where slang evolves quickly and the emotional meaning of words shifts faster than any static word list can track.

- What improvements would we make if we rebuilt it?:

	If rebuilding this dataset today, we would prioritize three changes:
	
	First, we would recruit a more demographically and linguistically diverse annotator pool which is ideally stratified by age, country, first language, and cultural background. Contested words will reflect genuine disagreement rather than annotator homogeneity. 
	
	Second, we would provide sentence level context alongside each word, allowing raters to score the word as it actually functions in use, not single word. 
	
	Third, we would build in a versioning and update mechanism, re rating a sample of words each year to track how emotional language changes over time. A hedonometer that cannot update itself becomes a historical artifact rather than a living instrument.


## How to run your code
- Setup steps
- Which scripts to run

## Credits
- Who did what (team roles)
- Citation for the paper / dataset
