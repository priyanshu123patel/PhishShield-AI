# PhishShield AI

PhishShield AI is a machine-learning powered web app that helps users quickly check whether a website URL appears legitimate or phishing.

Built with Flask and scikit-learn, the app extracts 30 URL/behavior features in real time, runs inference with multiple trained models, and returns an instant security prediction through a modern, responsive interface.

## Why This Project Stands Out

- Dual-model inference: switch between Random Forest and Decision Tree predictions.
- Real-time feature engineering: URL is normalized, parsed, and transformed into a phishing-risk feature vector.
- Live model score display: accuracy is evaluated from dataset labels when `phishing.csv` is available.
- UX-first design: polished, mobile-friendly frontend with quick sample URL testing chips.
- Practical security focus: fast feedback for awareness, demos, and educational use.

## Live App Flow

1. User submits a URL from the web form.
2. Backend validates and normalizes the input (`http://` is auto-added when missing).
3. System computes 30 phishing indicators (IP usage, URL length, redirects, subdomain depth, iframe behavior, and more).
4. Selected model predicts one of two outcomes:
   - `Legitimate Website`
   - `Phishing Website`
5. UI displays the prediction and currently selected model accuracy.

## Tech Stack

- Python
- Flask
- scikit-learn
- NumPy
- HTML/CSS/JavaScript

## Repository Structure

```text
PhishShield AI/
|- app.py
|- phishing.csv
|- phishing_model_rf.pkl
|- phishing_model_dt.pkl
|- phishing_website_detection_final_project.ipynb
|- requirements.txt
|- static/
|  |- logo.svg
|- templates/
|  |- index.html
|  |- developer.html
```

## Getting Started

### 1) Clone and enter project

```bash
git clone <your-repository-url>
cd "PhishShield AI"
```

### 2) Create and activate virtual environment (recommended)

Windows PowerShell:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Run the application

```bash
python app.py
```

Open your browser at:

```text
http://127.0.0.1:5000/
```

## Model Assets

The app expects both trained model files in the project root:

- `phishing_model_rf.pkl`
- `phishing_model_dt.pkl`

If either file is missing, model loading will fail at startup.

## Key Features Engineered in Backend

The prediction vector includes 30 attributes, such as:

- IP address usage in hostname
- long/short URL heuristics
- `@` symbol and redirect pattern checks
- prefix/suffix (`-`) analysis in domain
- subdomain depth scoring
- HTTPS and non-standard port checks
- suspicious page behaviors from fetched HTML (iframe, popup, right-click suppression, mouseover tricks)

This combination provides a practical heuristic + ML approach for phishing detection.

## Troubleshooting

- `ModuleNotFoundError`: run `pip install -r requirements.txt` again.
- `N/A` accuracy badge: verify `phishing.csv` exists and contains feature columns plus `class`.
- URL fetch-based checks not triggering: confirm internet connectivity (HTML fetch timeout is intentionally short).

## Security Note

PhishShield AI is an assistive detector, not a guaranteed verdict engine. Treat outputs as risk signals and always validate suspicious URLs with trusted security tools.

## Future Improvements

- Probability/confidence score display
- Batch URL scanning mode
- Model performance dashboard
- API endpoint for external integrations

## Author

Patel Priyanshu

Built with a focus on practical cybersecurity and user-friendly ML applications.
