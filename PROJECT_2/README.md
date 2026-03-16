# Mini-Project 2: Inferring Happiness Dynamics in Media

## 1. Project Overview

This project applies the **labMT hedonometer lexicon** to a corpus of movie reviews to measure emotional content in text. The goal is to estimate happiness scores for documents and examine how these scores relate to sentiment and rating.

We use the **IMDb Large Movie Review Dataset**, which contains 50,000 movie reviews labeled as positive or negative. By applying the hedonometer method to this dataset, we explore whether language associated with positive reviews produces higher happiness scores than language in negative reviews.


## 2. Repository Structure

repo/
│
├── README.md  
├── requirements.txt  
│  
├── src/  
│   ├── clean_imdb.py  
│   ├── hedonometer_scoring.py  
│   └── analysis_plots.py  
│  
├── data/  
│   ├── raw/  
│   │   └── imdb/  
│   │       ├── train/  
│   │       └── test/  
│   │  
│   └── processed/  
│       └── imdb_reviews_clean.csv  
│  
├── figures/  
│  
└── tables/  

Raw datasets are stored in `data/raw/`, while cleaned datasets used for analysis are stored in `data/processed/`.


## 3. Dataset

### IMDb Large Movie Review Dataset

The IMDb Large Movie Review Dataset contains **50,000 movie reviews** collected from IMDb.

Dataset characteristics:

- 25,000 training reviews
- 25,000 test reviews
- Balanced sentiment labels
- Positive reviews: rating ≥ 7
- Negative reviews: rating ≤ 4
- Neutral reviews are excluded

The dataset is distributed as individual text files organized into directories.

Dataset folder structure:

train/  
&nbsp;&nbsp;&nbsp;&nbsp;pos/  
&nbsp;&nbsp;&nbsp;&nbsp;neg/  

test/  
&nbsp;&nbsp;&nbsp;&nbsp;pos/  
&nbsp;&nbsp;&nbsp;&nbsp;neg/  

Each review file follows the naming convention:

[id]_[rating].txt

Example:

200_8.txt

This file corresponds to:
- review ID: 200
- rating: 8/10

<<<<<<< HEAD
=======
Sample:

- random sampling to limit bias
- fixed seed for reproducibility
- 200 reviews total : 50 pos reviews in train, 50 neg reviews in train, 50 pos reviews in test, 50 neg reviews in test
- to avoid a sample majorly positive or negative, we balanced positive and negative reviews 
- for a more representative sample, we balanced train and test
- Sanity checks: first few rows + counts
- Distribution checks: statistics and histograms of happiness score + of happiness score by sentiment : the sample reflects the dataset's distributions
- mean : 5.4325
- std : 0.1248
- min : 4.9130 
- max : 5.8932
- 25% : 5.3501
- 50% : 5.4250
- 75% : 5.5037
>>>>>>> 1ebcc5665ec07d520a927abe3af4c5208e088c14

## 4. Data Processing

To make the dataset usable for analysis, we convert the individual text files into a structured dataset.

Processing script:

src/clean_imdb.py

This script performs the following steps:

1. Iterates through the dataset directory structure (`train/test`, `pos/neg`)
2. Extracts metadata from filenames
3. Reads review text from each file
4. Stores the information in a pandas DataFrame
5. Saves the dataset as a single CSV file

The processed dataset contains one row per review.

Example dataset structure:

| review_id | rating | sentiment | split | text |
|-----------|--------|----------|-------|------|
| 200 | 8 | pos | test | this movie was amazing... |

The final dataset is saved as:

data/processed/imdb_reviews_clean.csv

Basic preprocessing steps include:

- removing newline characters
- trimming extra whitespace
- converting text to lowercase

<<<<<<< HEAD

## 5. Methods
=======
## 5. Estimand

- the estimand is the difference in mean happiness scores between positive and negative reviews
- population quantity: difference in mean sentiment between positive (rating ≥ 7) and negative reviews (rating ≤ 4)
- unit of analysis: individual IMDB review

## 6. Methods
>>>>>>> 1ebcc5665ec07d520a927abe3af4c5208e088c14

We apply the **hedonometer method** using the labMT lexicon.

Steps:

1. Tokenize each review into words
<<<<<<< HEAD
2. Match tokens with words in the labMT lexicon
3. Retrieve happiness scores for matched words
4. Compute the average happiness score for each review

This produces a document-level happiness estimate for each review.


## 6. Analysis



## 7. Visualizations


## 8. How to Run the Code


## 9. Tools Used
=======
2. Match tokens with words in the labMT lexicon. We will check which tokens from each review are present in the lexicon dictionary we made. 
3. For each token that exists in the lexicon, we retrieve its happiness score. 
4. Make a histograpm showing the distribution of happiness scores across all reviews. 
5. Make another plot comparing happiness scores for positive vs. negative reviews. 
6. Compute the average happiness score for each review

This produces a document-level happiness estimate for each review.

## 7. Analysis
The mean happiness scores are slightly above the midpoint where labMT scores range roughly from 1 to 9, with 5 as neutral.

# 8. Baseline descriptive comparison

- we compared the mean happiness score for positive and negative reviews in the sample
- mean happiness positive reviews: 5.49
- mean happiness negative reviews: 5.37
- baseline point estimate of the difference between positive and negative reviews: 0.12
- positive reviews thus present a slightly higher happiness score

# 9. Quantifying uncertainty

method:
- we used bootstrap resampling to quantify uncertainty for the average happiness score of both positive and negative reviews and for the baseline point estimate
- we resampled both positive and negative reviews with replacement 1000 times
- for each resample, we computed the mean happiness score
- we calculated the difference in means (positive - negative) for each bootstrap iteration 
- we calculated the 95% percentile confidence intervals for each group mean and the difference

results:
- 95% confidence interval for positive reviews: [5.47, 5.51]
- 95% confidence interval for negative reviews: [5.35, 5.40]
- 95% confidence interval for the difference in means (pos - neg): [0.09, 0.15]
- this confirms that positive reviews have a higher mean happiness score

To quantify our confidence in this effect, we estimated the probability that positive reviews have higher happiness scores than negative reviews: 
- probability: 1.00
- in all bootstrap iterations, positive reviews are happier than negative reviews
- this strongly supports our claim


## 10. Visualizations

### Distribution of Happiness Scores
![Happiness Score Histogram](figures/happiness_score_histogram.png)

This histogram shows the distribution of happiness scores across all IMDb reviews. Most reviews cluster around the middle range, with both ends of positive and negative tapering into extreme responses of sentiment. This helps us see the overall emotional positive and negative sentiments in the dataset.

### Happiness Scores by Sentiment
![Happiness Score by Sentiment](figures/happiness_score_by_sentiment.png)

This plot compares happiness scores for positive and negative reviews. Positive reviews tend to have higher happiness scores, while negative reviews cluster at lower scores. This demonstrates that the hedonometer method was a good option with modeling the sentiments in the IMDb dataset. 


### Mean Happiness CI 
![Mean Happiness CI](figures/mean_happiness_ci.png)

The positive reviews (mean = 5.49) scored higher than negative reviews. (mean = 5.37) The error bars show 95% bootstrap confidence intervals. Since the two intervals do not overlap, the difference is statistically meaningful. 

### Bootstrap Distribution by Sentiment 
![Bootstrap Difference Distribution](figures/bootstrap_difference_happiness_scores.png)

This histogram shows the bootstrap distribution of the difference in mean happiness scores (positive − negative) across 1,000 resamples. The observed mean difference (black dashed vertical line, 0.12) sits well above zero (red dashed vertical line), and the entire 95% CI [0.09, 0.15] (blue and green dashed vertical lines) lies above zero. This confirms that positive reviews consistently score higher than negative reviews, and the difference is unlikely to be due to chance.

### Bootstrap Distribution of Mean Happiness Scores
![Bootstrap Mean Happiness Scores](figures/bootstrap_mean_happiness_scores.png)

This plot shows the bootstrap distributions of mean happiness scores for positive (blue) and negative (orange) reviews across 1,000 resamples. The two distributions are completely separate with no overlap, and the 95% confidence intervals (shown by vertical dashed lines) do not intersect. Positive reviews consistently score higher (CI: [5.47, 5.51]) than negative reviews (CI: [5.35, 5.40]), which strongly supports our claim that sentiment label is associated with a meaningful difference in happiness score.

### Robustness Check

To verify the result is not driven by outliers, we repeated the comparison using the median instead of the mean:
- median happiness positive reviews: 5.47
- median happiness negative reviews: 5.37
- difference (median): 0.10

The finding holds under both estimators, confirming it is robust.

## 11. How to Run the Code


## 12. Tools Used
>>>>>>> 1ebcc5665ec07d520a927abe3af4c5208e088c14

- Python  
- pandas  
- numpy  
- matplotlib  
- GitHub for version control  

AI assistance was used to help debug code and clarify programming concepts.


<<<<<<< HEAD
## 10. Credits
=======
## 13. Credits
>>>>>>> 1ebcc5665ec07d520a927abe3af4c5208e088c14

Team members and roles:

- Repo & workflow lead:  
- Data acquisition lead:  
<<<<<<< HEAD
- Measurement lead:  
- Visualization lead:  
- Editor & figure curator:  


## 11. References
=======
- Measurement lead:
- Stats and sampling lead: Marguerite Audeguis (sampling plan (code, histograms and readme), quantifying uncertainty (code, histograms and some analysis))
- Visualization lead:  

## 14. References
>>>>>>> 1ebcc5665ec07d520a927abe3af4c5208e088c14

Maas, A. L., Daly, R. E., Pham, P. T., Huang, D., Ng, A. Y., & Potts, C. (2011).  
Learning Word Vectors for Sentiment Analysis. Proceedings of ACL 2011.

Dodds, P. S., et al. (2011).  
Temporal patterns of happiness and information in a global social network.
