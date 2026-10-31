# Dataset sources and expected files

Downloaded from the original UCI repository on 30 October 2026. The Kaggle preference was optional; using original sources gives a stable download without a Kaggle login. These are real observations, not generated substitutes. The small synthetic ordered-series demonstration is explicitly separate.

| File | Original source | Contents and attribution |
| --- | --- | --- |
| auto_mpg.csv | https://archive.ics.uci.edu/dataset/9/auto+mpg | 398 cars; Auto MPG, R. Quinlan, DOI 10.24432/C5859H. Source: CMU StatLib. |
| bank.csv | https://archive.ics.uci.edu/dataset/222/bank+marketing | Original published 4,521-row sample from bank.zip, not a newly generated subsample. Portuguese bank campaigns; S. Moro, P. Cortez, P. Rita. DOI 10.24432/C5K306. |
| reviews.csv | https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences | 1,000 real Yelp review sentences from the UCI collection by Dimitrios Kotzias. DOI 10.24432/C57604. Source publication: Kotzias et al., From Group to Individual Labels Using Deep Features, KDD 2015. |

Original source readmes and UCI metadata snapshots are retained in this folder. WordNet is distributed separately under its Princeton license, contained in data/nltk_data/corpora/wordnet.zip (LICENSE file inside the archive).

## Schema

- `auto_mpg.csv`: comma-delimited. Required numeric columns: mpg, cylinders, displacement, horsepower, weight, acceleration, model_year. Original origin and car_name are retained but unused. The original `?` missing markers become empty CSV cells. MPG is the regression target.
- `bank.csv`: **semicolon-delimited**, unchanged from UCI bank.zip. Required numeric columns: age, balance, campaign, pdays, previous. Required categorical columns: job, marital, education, default, housing, loan, contact, month, poutcome. Required target y: yes/no. Unknown string values become missing at load time. Extra day and duration columns are retained, but excluded from model inputs. Pdays=-1 is the documented 'not previously contacted' sentinel, not treated as a missing value.
- `reviews.csv`: comma-delimited, columns text and sentiment; sentiment=0 is negative and 1 is positive. Derived directly from yelp_labelled.txt; no generated reviews or fabricated labels. Duplicate/conflicting normalized text is removed before model splitting.

## Re-download

Run `python download_data.py` from the project root. This overwrites the three CSVs from the original archives. Run `python -m nltk.downloader -d data/nltk_data wordnet` only if WordNet is absent.

## License and attribution

Use and redistribution must follow the license listed by the original source. Links above identify the authoritative dataset pages; retain the attribution with submitted copies. See LICENSE_DATA.md for the verified dataset license notices.
