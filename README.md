# Machine Learning Lab — notebook first

**Start with `notebook/ML_Lab_Project.ipynb`.** It is the main project: all preprocessing, training, comparisons, evaluation, plots, interpretations and model export are written directly in its cells. It does not import the backend or any other project Python module.

The small website is only a demonstration of the required FastAPI + HTML/CSS/JavaScript connection. It has three forms: fuel efficiency, bank subscription and review sentiment. FastAPI loads the trained notebook pipelines; it never retrains models during a request.

## Python 3.14 setup fix

This version supports regular 64-bit CPython 3.14. The older pandas 2.2.3 pin tried to build from source on 3.14; the updated requirements use pandas 2.3.3, Pydantic 2.12.5 and ipykernel 7.4.0. Other direct package pins remain unchanged.

If the old setup failed, extract this updated ZIP into a fresh folder and run setup_windows.bat. You can keep Python 3.14 installed. If instead updating an existing folder, replace its three requirements text files and setup_windows.bat with the versions from this ZIP, then rerun setup. A regular 64-bit Python 3.14 .venv can be reused.

The setup now checks the Python version/architecture and requests prebuilt wheels, avoiding a local pandas compilation. The notebook outputs and model exports were regenerated under Python 3.14; see docs/COMPATIBILITY.md for exact verification.

## Easiest Windows setup — no commands to type

1. Install **64-bit Python 3.11–3.14** if necessary. On the Python installer, enable the launcher and Add Python to PATH.
2. Extract the ZIP. Open its **ml_lab** folder.
3. Double-click **setup_windows.bat**. It creates `.venv` and installs the pinned packages. Internet is needed for this first setup; XGBoost and Jupyter downloads can take several minutes. Keep the window open until it reports completion.
4. Double-click **start_notebook.bat**. Jupyter opens in your browser with **ML_Lab_Project.ipynb**. Keep its server window open while using Jupyter.
5. Read from the top. Use **Run → Run All Cells**, or run individual cells in order with Shift+Enter. The final cells save models, result tables and the report automatically.
6. To demonstrate the optional website, double-click **start_web.bat**, then open **http://127.0.0.1:8000**. Keep that server window open while using the page.

The notebook already has actual outputs and the three exported model files are included. You can inspect them immediately; rerun the notebook to learn the code and refresh the exports. Model training is not necessary merely to start the supplied website.

These batch launchers are provided for Windows, but were not directly tested on Windows in this environment. Error messages remain visible if setup fails. Only run project/model files you trust.

## If you prefer VS Code

Open the **ml_lab** folder, then `notebook/ML_Lab_Project.ipynb`. Install Microsoft's Python and Jupyter extensions if needed. Click **Select Kernel**, select the interpreter in this project's `.venv`, and use the Run Cell buttons. No FastAPI server is needed for notebook work.

Use `setup_windows.bat` once to install dependencies. You do not need to type terminal commands for the normal Windows workflow above.

## Manual setup / macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-notebook.txt
.venv/bin/python -m notebook notebook/ML_Lab_Project.ipynb
```

For the small website, in a separate terminal:

```bash
.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

On Windows the corresponding Python path is `.venv\Scripts\python.exe`.

To install only the website dependencies, use `requirements-web.txt`; the notebook needs the full notebook requirements. Notebook-only package downloads are unnecessary if you just want to inspect the supplied HTML report or run the website with its bundled models.

LightGBM may need `brew install libomp` on macOS, or the distribution's `libgomp1` runtime on minimal Linux. No GPU is needed.

## What to submit

- `notebook/ML_Lab_Project.ipynb`: main lab work, with actual outputs and plots.
- `backend/` and `frontend/`: minimal required web integration.
- `models/`: three exported complete pipelines and metadata.
- `data/`: real datasets, original sources, licenses and dictionary resource.
- `docs/REPORT.md` or `docs/REPORT.html`: brief report.
- This README and dependency lists.

`docs/CHECKLIST.md` maps every topic to a notebook section. `docs/VIVA_GUIDE.md` gives a short explanation of the design and key concepts.

## Folder structure

```text
ml_lab/
  notebook/ML_Lab_Project.ipynb   # all learning and training code
  backend/main.py                # load pipelines and return predictions
  frontend/index.html            # three small forms
  frontend/style.css
  frontend/app.js
  models/fuel_pipeline.joblib
  models/bank_pipeline.joblib
  models/sentiment_pipeline.joblib
  models/metadata.json
  data/                          # real CSVs, source/license files, WordNet
  results/notebook_results.json   # actual notebook result tables
  docs/REPORT.md
  docs/REPORT.html
  docs/CHECKLIST.md
  docs/VIVA_GUIDE.md
  docs/VALIDATION.md
  tests/check_app.py
  requirements-web.txt
  requirements.txt
  requirements-notebook.txt
  setup_windows.bat
  start_notebook.bat
  start_web.bat
  run_notebook.py                 # optional scripted notebook execution
  make_report_html.py
  download_data.py                # optional data recovery
```

## Notebook topics

The notebook covers missing-value methods, ordered filling, scaling, encoding, RFE/importance/PCA, simple/multiple/polynomial/Ridge/Lasso regression, regression metrics, logistic classification, thresholds/confusion/ROC, a separate vehicle boundary lesson, tree mathematics/pruning, forests/boosting, SVM kernels and C/gamma, Naive Bayes, imbalance/SMOTE/calibration, and text processing/sentiment.

The source data is real. Only the clearly labelled ordered-fill lesson is an invented time series; SMOTE separately creates synthetic *training* observations. Neither is disguised as collected real data.

## How models reach the website

1. The notebook fits a complete pipeline, including learned preparation.
2. Its export cell writes that pipeline into `models/` using joblib.
3. FastAPI loads it on the first request and reuses it.
4. JavaScript sends form inputs as JSON and displays the actual returned prediction.

Predefined export choices: multiple linear MPG; ordinary logistic subscription using five numeric features; TF-IDF unigrams/bigrams plus logistic sentiment. These choices are not automatically selected by the highest test score.

The website bank model is deliberately smaller than the notebook's full categorical/numeric classifier. Its threshold is displayed and adjustable. SVM models and all other comparisons remain in the notebook, where they are easier to explain.

After changing/re-exporting models, restart FastAPI to clear its in-memory model cache. `models/metadata.json` records evaluation values and package versions from the same run.

## Refresh results and report

Run all notebook cells. The final cells save `results/notebook_results.json`, three model files, metadata and `docs/REPORT.md`. `make_report_html.py` converts the report to printable HTML. Optional scripted alternative:

```bash
python run_notebook.py
python make_report_html.py
python tests/check_app.py
```

Use your `.venv` Python for those commands. The script executes notebook cells in-process using IPython and preserves their actual outputs; normal notebook use does not require it.

## Prediction API

Open http://127.0.0.1:8000/docs for interactive documentation.

| Route | Method | Purpose |
| --- | --- | --- |
| /api/status | GET | confirm exported files exist |
| /api/metadata | GET | inspect export settings and measured scores |
| /api/predict/fuel | POST | six vehicle features → estimated MPG |
| /api/predict/bank | POST | five numeric bank features + threshold → subscription probability/class |
| /api/predict/sentiment | POST | English review text → positive probability/class |

FastAPI serves the frontend at `/`, so CORS configuration is unnecessary for this same-origin arrangement. Use the server URL rather than double-clicking index.html. Loading, validation and missing-model errors are displayed; no frontend rule fabricates predictions when the API is unavailable.

## Troubleshooting

- **Python not found:** install 64-bit Python 3.11–3.14 and enable the launcher/PATH, then rerun setup.
- **Wrong notebook kernel:** select this project's `.venv` interpreter in Jupyter/VS Code.
- **Module missing:** rerun setup; avoid mixing packages from another environment.
- **Model missing:** run through the notebook's export cell, then restart the web server. The supplied ZIP already includes these files.
- **WordNet missing:** the dictionary is bundled. Restore `data/nltk_data/corpora/wordnet.zip` or use your environment's Python with `-m nltk.downloader -d data/nltk_data wordnet`.
- **Port in use:** close a previous web-server window, or manually start uvicorn on another port and use its address.
- **Zero minority recall:** this is a measured outcome at a particular threshold, not necessarily a code failure. Read the notebook's imbalance and SVM explanations.

Detailed verification and platform limitations are in `docs/VALIDATION.md`.
