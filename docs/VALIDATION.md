# Validation — notebook-first version

## Completed checks

- All 21 notebook code cells executed in order from a fresh in-process IPython namespace. Outputs include actual metric tables and plotted PNGs, not placeholders.
- The notebook is self-contained: it imports no backend/project modules. Its only local inputs are the supplied datasets and WordNet dictionary.
- Complete pipelines were exported by the notebook and loaded in a fresh backend process without notebook-defined classes or tokenizer functions.
- Fuel, bank and sentiment routes returned real predictions through FastAPI TestClient. Invalid values and blank text were rejected; missing-model behavior returned a readable 503 message.
- Static HTML, JavaScript and CSS were served successfully by FastAPI.
- All required model-comparison result groups were checked in the saved notebook results.
- Report Markdown and printable HTML were generated from actual notebook outputs.

## Verification limits

Tested on Linux with Python 3.12. Windows batch launchers are supplied but were not directly run on Windows. A Jupyter browser/kernel session was not launched here: this environment blocks the local network interfaces required for a separate Jupyter kernel. Code execution was verified in-process instead. Package notebook==7.4.3 is provided for the user's normal Jupyter launcher; its browser server is not claimed as tested here.

The preview runtime cannot run the Python ML packages, so live browser-to-FastAPI execution is not claimed. Any isolated frontend checks using captured real responses are documented below separately. Responsive/mobile behavior is not claimed as fully tested.

## Interpretation limits

Small historic datasets and repeated test comparisons support teaching, not an unbiased deployment benchmark. Numeric-only bank models differ from the full mixed-feature classifier. Some SVM probability thresholds give zero minority recall; those outcomes are retained and explained. The separate vehicle boundary is labelled as a different teaching task. LightGBM may emit a nonfatal transformed-array feature-name warning.

## Isolated browser checks

The unchanged three-form frontend was exercised in a browser using captured responses from actual successful FastAPI requests. Fuel prediction, subscription probability/threshold, positive and negative sentiment, and desktop result layout were checked. A deliberate 503 response displayed a clear error without inventing a fallback prediction. The fixture server was only a test harness and is not included in the submitted project. These checks do not claim a live browser-to-Python connection.


## Python 3.14 compatibility update

- Installed the full updated notebook requirements in a fresh Linux CPython 3.14.8 environment using prebuilt wheels only.
- Executed all 21 notebook code cells successfully under that interpreter. Saved outputs, result tables, pipelines and report now reflect that run.
- All three prediction routes, error behavior and coverage checks passed under Python 3.14.8.
- The same exported models and API checks also passed under Python 3.12 after updating the three changed dependency pins.
- The complete requirements resolved for Windows x64 Python 3.14 with binary-only packages, including compiled transitive dependencies. This confirms compatible installers exist, not that the Windows batch launcher was executed here.
- The user's exact Python 3.14.2 Windows installation remains to be confirmed locally. No promise is made about arbitrary future Python versions.
