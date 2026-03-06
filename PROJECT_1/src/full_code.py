"""
This is the complete code for project analysis. 
All in one place: loading and cleaning the data, doing the analysis, and creates plots and tables.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


# Step 10. labMT words appearance 
twitter_count = df['twitter_rank'].notna().sum() # df[] allows us to select a specific column ; .notna() allows us to exclude missing values ; .sum() counts the number of non-missing values in the column
google_count = df['google_rank'].notna().sum()
nyt_count = df['nyt_rank'].notna().sum()
lyrics_count = df['lyrics_rank'].notna().sum()

print(f"Missing values in Twitter Rank: {df['twitter_rank'].isna().sum()}") # This is a sanity check to see how many (.sum()) missing values (.isna()) there are in the twitter_rank column
print(f"Number of labMT words appearing in Twitter: {twitter_count}")
print(f"Number of labMT words appearing in Google: {google_count}")
print(f"Number of labMT words appearing in NYT: {nyt_count}")
print(f"Number of labMT words appearing in Lyrics: {lyrics_count}") #We print the number of labMT words appearing in each corpus

word_counts_table = pd.DataFrame({ # creating a dataframe with the results
    "Corpus": ["Twitter", "Google Books", "NYT", "Lyrics"], # defining the first column with the corpus names and naming it "corpus"
    "Number_of_labMT_words": [twitter_count, google_count, nyt_count, lyrics_count] # defining the second column with the word counts and naming it "Number_of_labMT_words"
})

word_counts_table.to_csv('tables/labMT_word_counts.csv', index=False) #saving the table as a csv file in the tables folder, without the index column

#Step 11. Overlap table 
df["T"] = df["twitter_rank"].notna() # creating new columns for each corpus, where the value is True if the word appears in that corpus (notna()) and False if it does not (na)
df["G"] = df["google_rank"].notna()
df["N"] = df["nyt_rank"].notna()
df["L"] = df["lyrics_rank"].notna()

overlaps = {} # creating an empty dictionary to store the counts of overlaps between the corpora

# Single corpus only
overlaps["T only"] = (df["T"] & ~df["G"] & ~df["N"] & ~df["L"]).sum() # counting the number of words that appear only in Twitter (T is True, G, N, L are False)
overlaps["G only"] = (~df["T"] & df["G"] & ~df["N"] & ~df["L"]).sum() # same logic for G
overlaps["N only"] = (~df["T"] & ~df["G"] & df["N"] & ~df["L"]).sum() # same logic for N
overlaps["L only"] = (~df["T"] & ~df["G"] & ~df["N"] & df["L"]).sum() # same logic for L

# Pairwise only
overlaps["T+G"] = (df["T"] & df["G"] & ~df["N"] & ~df["L"]).sum() # counting the number of words that appear in both Twitter and Google (T and G are True), but not in NYT or Lyrics (N and L are False)
overlaps["T+N"] = (df["T"] & df["N"] & ~df["G"] & ~df["L"]).sum() # same logic 
overlaps["T+L"] = (df["T"] & df["L"] & ~df["G"] & ~df["N"]).sum()
overlaps["G+N"] = (df["G"] & df["N"] & ~df["T"] & ~df["L"]).sum()
overlaps["G+L"] = (df["G"] & df["L"] & ~df["T"] & ~df["N"]).sum()
overlaps["N+L"] = (df["N"] & df["L"] & ~df["T"] & ~df["G"]).sum()

# Three-way only
overlaps["T+G+N"] = (df["T"] & df["G"] & df["N"] & ~df["L"]).sum() # counting the number of words that appear in Twitter, Google, and NYT (T, G, N are True), but not in Lyrics (L is False)
overlaps["T+G+L"] = (df["T"] & df["G"] & df["L"] & ~df["N"]).sum() # same logic
overlaps["T+N+L"] = (df["T"] & df["N"] & df["L"] & ~df["G"]).sum()
overlaps["G+N+L"] = (df["G"] & df["N"] & df["L"] & ~df["T"]).sum()

# All four
overlaps["T+G+N+L"] = (df["T"] & df["G"] & df["N"] & df["L"]).sum() # counting the number of words that appear in all four corpora (T, G, N, L are all True)

overlap_table = pd.DataFrame.from_dict(overlaps, orient="index", columns=["Count"]) # converting the overlaps dictionary into a dataframe, where the keys of the dictionary become the index of the dataframe and the values become a column named "Count"
print(overlap_table) 

overlap_table.to_csv('tables/overlap_table.csv') # saving the overlap table as a csv file in the tables folder

#Step 12. Twitter rank VS NYT rank scatterplot
both = df[ # creating a subset that includes only the words that appear in both Twitter and NYT
    df["twitter_rank"].notna() & # selecting only the rows where the twitter_rank is not missing
    df["nyt_rank"].notna() # same logic
]

plt.figure() # creating a new figure for the plot, to avoid plotting on top of any previous plots

plt.scatter( # creating a scatterplot 
    both["twitter_rank"], # using the twitter_rank column for the x-axis
    both["nyt_rank"] # using the nyt_rank column for the y-axis
)

plt.xlabel("Twitter Rank") # labeling the x-axis as "Twitter Rank"
plt.ylabel("NYT Rank") # labeling the y-axis as "NYT Rank"
plt.title("Twitter Rank vs NYT Rank (Words Present in Both)") # adding a title

plt.tight_layout()
plt.savefig("figures/twitter_vs_nyt_scatter.png") # saving the scatterplot as a png file in the figures folder
plt.close()