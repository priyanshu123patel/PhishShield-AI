# PhishShield AI

PhishShield AI is a Flask-based web app that predicts whether a URL is likely **Legitimate** or **Phishing** using a pre-trained machine learning model.

## Features

- URL phishing detection from a simple web interface
- Automatic feature extraction from the submitted URL
- Model prediction output:
  - Legitimate Website
  - Phishing Website
- Displays model accuracy calculated from `phishing.csv` (when available)
- Includes sample URLs for quick testing

## Project Structure

- `app.py` - Flask application and URL feature extraction logic
- `templates/index.html` - Frontend UI
- `static/` - Static assets (logo, etc.)
- `phishing_model.pkl` - Trained phishing detection model
- `phishing.csv` - Dataset used for local accuracy display
- `phishing_website_detection_final_project.ipynb` - Notebook used during model development/training

## Requirements

- Python 3.8+
- pip

Python packages:

- Flask
- scikit-learn

You can install dependencies with:

```bash
pip install flask scikit-learn
```

## Run Locally

1. Open a terminal in the project folder.
2. Start the app:

```bash
python app.py
```

3. Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## How It Works

1. You submit a URL from the homepage.
2. The app normalizes and parses the URL.
3. It extracts 30 phishing-related features (such as URL length, use of IP, HTTPS, special symbols, and page behavior hints).
4. The feature vector is passed to the trained model loaded from `phishing_model.pkl`.
5. The app returns a prediction on the UI.

## Important Notes

- This tool provides an ML-based estimate, not a guaranteed verdict.
- Some features depend on short HTML fetches and may be limited by connectivity/timeouts.
- Keep `phishing_model.pkl` and `phishing.csv` in the project root so the app can load them correctly.

## Troubleshooting

- If you see import errors, reinstall dependencies:

```bash
pip install --upgrade flask scikit-learn
```

- If model loading fails, ensure `phishing_model.pkl` exists in the root folder.
- If accuracy shows `N/A`, ensure `phishing.csv` exists and has the expected columns.

## Disclaimer

Use this project for educational and defensive security purposes. Always verify suspicious links with trusted security tools before visiting or sharing them.
