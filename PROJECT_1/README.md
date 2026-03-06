# Hedonometer

This project combines qualitative and quantitative methods to explore the labMT 1.0 dataset, in which the 5000 most common words in Google Books, New York Times articles, Music Lyrics and Twitter posts are combined and assigned a happiness score. This analysis of the labMT 1.0 dataset aims at mapping the expression of happiness on Twitter while critically engaging with the dataset. 

## Dataset section

### Summary Statistics for Happiness Average
They were computed in full_code.py 
Here are the computed summary statistics for the happiness_average column:
- Mean: 5.38
- Median: 5.44
- Standard deviation: 1.08
- 5th percentile: 3.18
- 95th percentile: 7.08
These numbers help us understand the overall distribution of happiness scores in the dataset. 

- Where it came from: labMT 1.0 dataset (Hedonometer project)
- What each column means (data dictionary):
	- We made a data dictionary to help us understand what each column in the dataset represents, what type of data it is, and how many missing values there are. It is useful because it clarifies the dataset and helps us know what to look for when analyzing or plotting data. 
	- Here’s a summary of the columns' names with float and integer:
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
We checked the dataset for any duplicated words. This is important because duplicates could skew our analysis and commpromise our results. Our check found that there are no duplicated words in the dataset, so each word only appears once. This gives us confidence that the data is clean and ready for analysis! The most positive words are: laughter, happiness, love, happy, laughed, laugh, laughing, excellent, laughs, and joy. The most negative words are: terrorist, suicide, rape, terrorism, murder, death, cancer, died, kill, and killed. These associations make sense, which confirms that the dataset is usable. 

### Why take a random sample?
- We took a random sample of 15 rows from the dataset to get a snapshot of the kind of data we are working with. It lets us see some real examples. It also helps check for any obvious issues, like weird values or repeated words.
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

All analysis was performed in python using the pandas, numpy, and matplotlib libraries. The workflow is implemented in the script 'src/o1_load_and_clean.py'. 

### Data processing
The labMT 1.0 dataset was loaded into a pandas DataFrame from a tab-delimited file. Metadata lines at the top of the file were skipped, and the placeholder value "--" was interpreted as missing data. Numeric columns such as happuness scores and corpus were converted to numeric data types to allow statistical analysis. 

### Descriprive statistics and distribution analysis
Summary statistics were calculated for the 'happiness_average' column, including the mean, median, and standard deviation, and percentile values. A histogram of happiness scores was generated to visualise the overall distribution of emotional valence across words. 

### Disagreement analysis 
To explore disagrement among annotators, a scatterplot of 'happiness_average' versus 'happiness_standard_deviation' was created. Words with the highest standard deviation were identified as the most contested words in the dataset and saved to a table. 

### Corpus comparison
The dataset includes rank columns for four corpora: Twitter, Google Books, the New York Times, and song lyrics. For each corpus, the number of words appearing in the top 5000 was counted. Boolean indicators were then used to calculate overlap patterns between corpora, identifying words shared across different sources 

### Cross-corpus frequency comparison 
A scatterplot comparing 'twitter_rank' and 'nyt_rank' was generated for words appearing in both corpora. This allows visual comparison between informal social media language and more formal news writing. 

## Results section
### Histogram Interpretation
The histogram of happiness_average scatter plot under the figures folder shows the happiness score is out of 10 along the bottom (where 10 is the happiest). The frequency is out of the total number of words in your dataset. At first glance, the scatter plot looks like a bird in flight with wings on either side where words are shown least on each side and the body of the bird is most rounded and clustered. SURPRISINGLY, the distribution is slightly skewed toward positive values around the 6 score being that average people are feeling a 6 in happiness scale. It could also mean there are more happy words than sad ones. There are rarely word with extremely low happiness scores between 1 or 2 which suggests this particular random selection has been generally happy.

#### Corpus comparison: 
Words appearances: 
For each corpus, 5000 labMT 1.0 words appear in its top 5000 words. This implies that the labMT 1.0 dataset was produced by merging the 5000 most common words on Twitter, Google Books, the New York Times and Music Lyrics.

Words overlaps: 
We analysed the amount of words that appear in each separate corpus and in all four corpuses combined, but also how many words are shared by every comibination of two and three corpuses. 

Lyrics present the highest amount of unique words (1486) and Twitter the lowest (952), while Google Books and the NYT seat in the middle, with respectively 1115 and 1043 original words. This implies that Lyrics' vocabulary is the most atypical, while Twitter shares a vast majority of its vocabulary with the other corpora. The large presence of unique words in the Lyrics' corpus could be due to their informality. 

Twitter shares 69 words with Google Books, 268 words with the NYT, and 871 with Lyrics. As Twitter presents the lowest number of unique words, these results entail that vocabulary is the most different between Twitter and Google Books. This could be due to the use of more formal vocabulary on Google Books. On the other hand, Twitter shares a large portion of words with Lyrics, probably because the two corpora both contain informal language. 

Google Books shares 864 words with the NYT and 175 with Lyrics. The fact that Google Books shares the most words with the NYT can once again be understood as a similar style of language.

The NYT has only 62 words in common with Lyrics. Twitter, Google Books and the NYT share 584 words. Twitter, Google Books and Lyrics share 227 words. Twitter, the NYT and Lyrics have 213 words in common. Google Books, the NYT and Lyrics present the lowest overlap with 150 shared words.

Finally, all four corpuses have 1816 words in common in their top 5000. 

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
### Setup Steps 
1. Clone the repository.
2. Create a virtual environment.
3. Install required packages.
(pip install -r requirements.txt)
4. Ensure the dataset is in the correct location.
The raw dataset file should be placed in data/raw/Data_Set_S1.txt
5. From the src folder, run full_code.py.
6. Running the script will:
	- Load and clean the dataset.
	- Save the cleaned dataset to data/clean/clean_data csv. 
	- Generate figures saved in figures/.
	- Generate tables saved in tables/. 

## Credits
- Who did what (team roles)
	- Anastasia Ciorogaru: Repo & Workflow Lead & Figure Curator
		- created and organized the repository, cleaned up code and README, managed branches and helped stay organized
		- additionally, wrote the code for dataset cleanup (loaded dataset, handled missing values, converted data types), completed the methods section in the README, and performed the write-up the tasks for the word "exhibit". 
	- Catalina Mena Llopez: Qualitative / Close Reading
		- lead interpretation of selected words, performed sanity checks, helped with distribution of happiness scores
		- connected qualitative observations back to patterns in the plots
		- created citation list
	- Yoonkyung Kim: Provenance & Critique Lead
		- reconstructed the dataset pipeline
		- wrote the 'critical reflection' sections: consequence, bias, limitations, and what the dataset makes easy/hard to see. 
	- Marguerite Audeguis: Quantitative Analyst
		- led descriptive statistics, and created plots
		- checked results for sanity and reproducibility
		- additionally wrote code and interpretation for corpus comparison, and the project overview
	- Hena Puthengot
	
- Citation for the paper / dataset
Hedonometer. "About." https://hedonometer.org/about.html