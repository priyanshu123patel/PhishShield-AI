from flask import Flask, redirect, render_template, request, url_for
import csv
import ipaddress
import pickle
import re
import urllib.parse
import urllib.request

app = Flask(__name__)

model = pickle.load(open("phishing_model.pkl", "rb"))


def _get_model_accuracy_text(csv_path="phishing.csv"):
    """Return dataset accuracy text for display, if dataset is available."""
    try:
        X = []
        y = []
        with open(csv_path, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Dataset has an Index column and a class label; model uses the remaining 30 features.
                X.append([float(row[name]) for name in reader.fieldnames if name not in {"Index", "class"}])
                y.append(int(float(row["class"])))

        if not X:
            return "N/A"

        accuracy = model.score(X, y) * 100.0
        return f"{accuracy:.2f}%"
    except Exception:
        return "N/A"


MODEL_ACCURACY = _get_model_accuracy_text()


def _safe_open_url(url):
    """Fetch HTML with a short timeout; return empty string if unavailable."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _is_ip(hostname):
    try:
        ipaddress.ip_address(hostname)
        return True
    except Exception:
        return False


def extract_features_from_url(raw_url):
    url = raw_url.strip()
    if not url:
        raise ValueError("Please enter a URL.")

    if not re.match(r"^https?://", url, flags=re.IGNORECASE):
        url = "http://" + url

    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    html = _safe_open_url(url)

    if not hostname:
        raise ValueError("Invalid URL. Try a full website address.")

    shorteners = {
        "bit.ly",
        "goo.gl",
        "tinyurl.com",
        "t.co",
        "is.gd",
        "ow.ly",
        "rb.gy",
        "cutt.ly",
        "shorturl.at",
    }

    domain_dots = hostname.count(".")
    has_redirect_pattern = "//" in parsed.path or "//" in parsed.query
    is_https = parsed.scheme.lower() == "https"

    using_ip = -1 if _is_ip(hostname) else 1
    url_len = len(url)
    if url_len < 54:
        long_url = 1
    elif url_len <= 75:
        long_url = 0
    else:
        long_url = -1

    short_url = -1 if any(s in hostname.lower() for s in shorteners) else 1
    symbol_at = -1 if "@" in url else 1
    redirecting = -1 if has_redirect_pattern else 1
    prefix_suffix = -1 if "-" in hostname else 1

    if domain_dots <= 1:
        subdomains = 1
    elif domain_dots == 2:
        subdomains = 0
    else:
        subdomains = -1

    https_feature = 1 if is_https else -1
    domain_reg_len = 0
    favicon = 0
    non_std_port = -1 if parsed.port and parsed.port not in (80, 443) else 1
    https_domain_url = -1 if "https" in hostname.lower() else 1

    request_url = 0
    anchor_url = 0
    links_script_tags = 0
    server_form_handler = 0
    info_email = -1 if re.search(r"mailto:", html, flags=re.IGNORECASE) else 1

    abnormal_url = 1 if hostname.lower() in url.lower() else -1
    website_forwarding = 0
    statusbar_cust = -1 if "onmouseover" in html.lower() else 1
    disable_right_click = -1 if "contextmenu" in html.lower() else 1
    popup_window = -1 if "window.open" in html.lower() else 1
    iframe_redirection = -1 if "<iframe" in html.lower() else 1
    age_of_domain = 0
    dns_recording = 0
    website_traffic = 0
    page_rank = 0
    google_index = 0
    links_pointing_to_page = 0
    stats_report = 0

    features = [
        using_ip,
        long_url,
        short_url,
        symbol_at,
        redirecting,
        prefix_suffix,
        subdomains,
        https_feature,
        domain_reg_len,
        favicon,
        non_std_port,
        https_domain_url,
        request_url,
        anchor_url,
        links_script_tags,
        server_form_handler,
        info_email,
        abnormal_url,
        website_forwarding,
        statusbar_cust,
        disable_right_click,
        popup_window,
        iframe_redirection,
        age_of_domain,
        dns_recording,
        website_traffic,
        page_rank,
        google_index,
        links_pointing_to_page,
        stats_report,
    ]

    return features, url

@app.route('/')
def home():
    prediction_text = request.args.get("prediction", "")
    error_text = request.args.get("error", "")
    return render_template(
        'index.html',
        prediction_text=prediction_text,
        entered_url="",
        error_text=error_text,
        model_accuracy=MODEL_ACCURACY,
    )


@app.route('/developer')
def developer():
    return render_template('developer.html')

@app.route('/predict', methods=['POST'])
def predict():
    raw_url = request.form.get("url", "")

    try:
        features, _ = extract_features_from_url(raw_url)
        prediction = model.predict([features])

        if prediction[0] == 1:
            result = "Legitimate Website"
        else:
            result = "Phishing Website"

        return redirect(url_for("home", prediction=result))
    except Exception as exc:
        return redirect(url_for("home", error=f"Error: {exc}"))

if __name__ == "__main__":
    app.run(debug=True)