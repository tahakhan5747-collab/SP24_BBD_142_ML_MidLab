# Dataset license notices

The original UCI pages for all three datasets explicitly link to Creative Commons Attribution 4.0 International (CC BY 4.0). The links were checked on 30 October 2026.

- Auto MPG: https://archive.ics.uci.edu/dataset/9/auto+mpg — R. Quinlan, DOI 10.24432/C5859H.
- Bank Marketing: https://archive.ics.uci.edu/dataset/222/bank+marketing — S. Moro, P. Cortez and P. Rita, DOI 10.24432/C5K306.
- Sentiment Labelled Sentences: https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences — Dimitrios Kotzias, DOI 10.24432/C57604.

License: https://creativecommons.org/licenses/by/4.0/  
Legal code: https://creativecommons.org/licenses/by/4.0/legalcode

CC BY 4.0 permits sharing and adaptation, with appropriate attribution, a license link and indication of changes. No endorsement by the data authors is implied. Other rights such as privacy are not automatically granted by that license.

Changes in the supplied files: Auto MPG was converted from whitespace format to CSV with missing markers represented as empty cells; bank.csv is the unchanged published UCI sample; Yelp text/label lines were converted to text,sentiment CSV columns. Model loading handles missing values and duplicate reviews as described in SOURCES.md. The source readmes remain included.

WordNet dictionary data is included at data/nltk_data/corpora/wordnet.zip. Its separate Princeton WordNet license is retained inside the archive at wordnet/LICENSE. WordNet is a dictionary resource, not a fourth observational dataset.
