# Machine Learning Lab Midterm Project

**Taha Ali Khan · BS Business Data Analytics · Semester 5 · COMSATS University Islamabad**

## Objective and datasets

The self-contained Jupyter notebook is the main project. It performs preprocessing, training, evaluation and visualization, and exports three pipelines. A minimal FastAPI backend loads them for fuel, subscription and sentiment prediction through one HTML/CSS/JavaScript page.

Real datasets: UCI Auto MPG (398 cars), published Bank Marketing sample (4,521 customers), Yelp labelled sentences (1,000 before deduplication). Sources and licenses: data/SOURCES.md. A separate seven-day filling example is explicitly synthetic; SMOTE creates synthetic training examples only.

## Method and preprocessing

Seed 42; 75/25 split; classification/text stratified. Preparation fits only training data. Call duration is excluded. Duplicate/conflicting texts are removed before splitting. Demonstrations cover deletion, mean/median/mode/KNN, ordered filling/interpolation, three scalers, label/one-hot/frequency encoding, RFE, importance and PCA.

| method | train_replacement | test_missing_after |
| --- | --- | --- |
| mean | 103.2116 | 0 |
| median | 92.0000 | 0 |
| most_frequent | 90.0000 | 0 |

| component | variance_explained |
| --- | --- |
| 1 | 0.3257 |
| 2 | 0.2162 |

Interpretation: imputation retains observations; feature selection reduces inputs, while PCA makes meanings less direct. Backward filling/interpolation can use future observations.

## Regression

| model | r2 | mae | rmse |
| --- | --- | --- | --- |
| Simple linear | 0.7277 | 3.2109 | 3.9320 |
| Multiple linear | 0.8272 | 2.5292 | 3.1325 |
| Polynomial degree 2 | 0.7626 | 2.8433 | 3.6717 |
| Ridge | 0.8273 | 2.5300 | 3.1313 |
| Lasso | 0.8338 | 2.3900 | 3.0724 |
| Regression tree | 0.7915 | 2.4084 | 3.4408 |

Interpretation: lower held-out MPG errors support fuel-cost estimates. The degree comparison in the notebook illustrates that improved training fit does not guarantee better generalization. Historic cars do not establish modern-fleet performance.

## Classification and trees

| threshold | precision | recall | f1 | fp | fn |
| --- | --- | --- | --- | --- | --- |
| 0.2000 | 0.3277 | 0.3000 | 0.3133 | 80 | 91 |
| 0.3000 | 0.4000 | 0.2154 | 0.2800 | 42 | 102 |
| 0.5000 | 0.5405 | 0.1538 | 0.2395 | 17 | 110 |
| 0.7000 | 0.6250 | 0.0769 | 0.1370 | 6 | 120 |

| model | accuracy | f1 | roc_auc |
| --- | --- | --- | --- |
| Tree Gini | 0.8727 | 0.2800 | 0.6077 |
| Tree entropy | 0.8727 | 0.2800 | 0.6477 |
| Unrestricted tree | 0.8152 | 0.2172 | 0.5576 |
| Pruned tree | 0.8806 | 0.2932 | 0.6653 |
| Random forest | 0.8904 | 0.1842 | 0.7046 |
| AdaBoost | 0.8904 | 0.2250 | 0.7055 |
| Gradient boosting | 0.8904 | 0.2530 | 0.7129 |
| XGBoost | 0.8824 | 0.2036 | 0.6962 |
| LightGBM | 0.8859 | 0.2367 | 0.6998 |

Interpretation: lower thresholds may find subscribers while increasing unnecessary calls. Trees offer readable rules; forests combine bagging and random features; boosting adds learners sequentially. The notebook calculates entropy, Gini and information gain at a real tree root and compares pruning. Its vehicle boundary is a separate lesson, not bank-model performance.

## SVM, Naive Bayes and imbalance

| model | precision | recall | f1 | roc_auc |
| --- | --- | --- | --- | --- |
| SVM linear | 0.0000 | 0.0000 | 0.0000 | 0.4520 |
| SVM polynomial | 0.0000 | 0.0000 | 0.0000 | 0.5363 |
| SVM RBF | 0.0000 | 0.0000 | 0.0000 | 0.5526 |
| RBF balanced | 0.0000 | 0.0000 | 0.0000 | 0.6474 |
| Gaussian NB | 0.2072 | 0.1769 | 0.1909 | 0.6250 |
| RBF unscaled | 0.0000 | 0.0000 | 0.0000 | 0.4270 |

| model | precision | recall | f1 | brier |
| --- | --- | --- | --- | --- |
| Majority baseline | 0.0000 | 0.0000 | 0.0000 | 0.1017 |
| Logistic baseline | 0.1429 | 0.0077 | 0.0146 | 0.1020 |
| Class weighting | 0.1711 | 0.4462 | 0.2473 | 0.2393 |
| SMOTE | 0.1685 | 0.4692 | 0.2480 | 0.2384 |
| Weighted + calibration | 0.1250 | 0.0077 | 0.0145 | 0.1025 |
| Baseline threshold 0.3 | 0.1429 | 0.0231 | 0.0397 | 0.1020 |

Interpretation: numeric-only SVM/NB and imbalance inputs differ from the full bank classifier. Scaling and C/gamma affect kernels. Gaussian NB has imperfect normality/independence assumptions. Zero minority recall is a real result; SVM margins and probability thresholds can disagree. Weighting/SMOTE trade recall against precision. Whole-pipeline training-fold calibration can improve probability reliability but is not guaranteed to do so.

## Text analysis

| model | accuracy | f1 | roc_auc |
| --- | --- | --- | --- |
| Bag of words | 0.8072 | 0.8065 | 0.8890 |
| Stop words removed | 0.8193 | 0.8207 | 0.8951 |
| TF-IDF | 0.7751 | 0.7686 | 0.8699 |
| TF-IDF bigrams | 0.7871 | 0.7871 | 0.8641 |
| Stemming | 0.7791 | 0.7737 | 0.8760 |
| Lemmatization | 0.8032 | 0.7950 | 0.8836 |
| TF-IDF max_df=0.3 | 0.7952 | 0.7918 | 0.8752 |
| Linear SVM calibrated | 0.8112 | 0.8082 | 0.8978 |
| Multinomial NB alpha=1 | 0.7791 | 0.7843 | 0.8823 |
| Multinomial NB alpha=0.1 | 0.8032 | 0.8000 | 0.8813 |

Interpretation: real negative feedback can be flagged for human review. The notebook compares counts, TF-IDF, n-grams, negation-preserving stop words, max_df, stemming/lemmatization, LinearSVC and Laplace smoothing. Small English sentences do not establish accuracy for sarcasm, Urdu or new domains.

## Integration and limitations

The notebook exports complete sklearn pipelines; FastAPI loads them without training. The page sends validated JSON and displays actual predictions. No fallback invents model outputs. Deployment choices are predefined, not chosen using the test winner. The web bank model deliberately uses five numeric features and a stated threshold.

These are small historical benchmarks, not real-world validation or causal evidence. Repeated test comparisons are classroom demonstrations, not unbiased final model selection. Windows and live browser-to-Python verification limits are recorded in docs/VALIDATION.md.

## Sources

Auto MPG: https://archive.ics.uci.edu/dataset/9/auto+mpg  
Bank Marketing: https://archive.ics.uci.edu/dataset/222/bank+marketing  
Sentiment Labelled Sentences: https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences