# Requirement coverage — notebook-first version

The main file is `notebook/ML_Lab_Project.ipynb`. All modelling code is directly visible; it imports no backend modules.

| Required activity | Notebook section / deliverable |
| --- | --- |
| Real suitable datasets and EDA | §2: three real CSVs, previews, descriptive statistics, missing counts, class distribution plot; data/SOURCES.md |
| Train/test before learned preparation | §3: seed 42, 75/25 split; bank/text stratified |
| Deletion, mean/median/mode | §4: real missing horsepower; train-only replacement statistics |
| Categorical mode | §4: real unknown education values converted to missing |
| KNN imputation | §4: neighbors on scaled training features |
| Forward fill, backward fill, interpolation | §4: explicitly synthetic seven-day ordered series; never model input |
| Min-Max, standardization, robust scaling | §5: test rows transformed with training statistics |
| Label, one-hot, count/frequency encoding | §5: train-only vocabulary/mapping; feature labels are demonstration-only |
| RFE, tree importance, PCA | §6: selected numeric features, rankings, explained variance and scatter |
| Simple/multiple/polynomial/Ridge/Lasso | §7: real MPG target, six-model table including regression tree |
| Underfitting/overfitting and R²/MAE/RMSE | §7: degree 1–15 training/test RMSE plot and actual/predicted scatter |
| Logistic probabilities and thresholds | §8: full mixed-feature bank classifier, fixed threshold comparison |
| Confusion matrix, accuracy, precision, recall, specificity, F1, ROC-AUC | §8: correctly labelled matrix, metric tables and ROC plot; reusable metric helper §1 |
| Decision boundary | §8: clearly separate weight/horsepower → ≥6-cylinder lesson using real Auto MPG observations |
| Gini, entropy, weighted child impurity, information gain | §9: actual training tree root calculation |
| Tree rules, classification/regression trees, pruning | §7 regression tree; §9 extracted rules, limited/unrestricted/post-pruned classification trees |
| Random Forest, bagging, random features | §9: training and explanation |
| AdaBoost, gradient boosting, XGBoost, LightGBM | §9: all five ensemble comparisons with measured results |
| Linear/polynomial/RBF SVM, C/gamma, scaling | §10: small numeric-feature experiment, scaling contrast and sensitivity table |
| Naive Bayes, Bayes rule and conditional independence | §10 Gaussian NB; §12 Multinomial NB |
| Laplace smoothing | §12: Multinomial NB alpha 1 versus 0.1 |
| Imbalance baseline, class weights, SMOTE | §11: majority/logistic baselines, weights and training-only numeric SMOTE |
| Threshold change and probability calibration | §11: fixed 0.3 threshold, whole-pipeline training-fold calibration, Brier and reliability plot |
| Tokens, counts, sparse vocabulary, stop words, TF-IDF | §12: actual training-review features, formula, negation-preserving stop list |
| N-grams, stemming, lemmatization | §12: unigrams/bigrams, Porter and WordNet comparisons |
| Sentiment classifier, influential terms, unknown terms | §12: ten models, signed coefficients, editable review example, unknown-term count |
| Train and save complete model pipelines | §13: three joblib files + evaluation metadata; files included |
| FastAPI backend | backend/main.py: validation, model loading and three prediction routes; no training code |
| HTML/CSS/JavaScript frontend | frontend/: single page, three forms, fetch/JSON integration, actual predictions and clear errors |
| Setup/source/report | README, batch launchers, pinned requirements, §14 generated report and results/notebook_results.json |

The slides contain explanations and worked examples rather than one numbered practical sheet. This project applies the concepts to appropriate real datasets rather than reproducing fictional business numbers. SVM remains small because its roadmap says theory only. LDA/topic modelling is described as the next textbook topic and is not included as an additional activity.
