from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# Load model
import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
nltk.download('stopwords')
s=set(stopwords.words("english"))
le=WordNetLemmatizer()

def preprocess(x):
    l=x.lower()
    t=nltk.word_tokenize(l)
    p=[i for i in t if i not in string.punctuation]
    sw=[i for i in p if i not in s ]
    t_l=[le.lemmatize(i) for i in sw]
    return ' '.join(t_l)

model = joblib.load("spam_classifier.pkl")

@app.route("/")
def index():
    return send_from_directory("static", "spamfront.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


@app.route("/predict", methods=["POST"])
def predict_text():
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "Empty input"}), 400

    # Use model pipeline to predict probability
    text = preprocess(text)
    prob = model.predict_proba([text])[0]
    pred_class = model.predict([text])[0]

    response = {
        "prediction": "Ham" if pred_class == 1 else "Spam",
        "probability_spam": round(float(prob[0]), 3),
        "probability_ham": round(float(prob[1]), 3)
    }

    return jsonify(response)

@app.route("/predict-csv", methods=["POST"])
def predict_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    df = pd.read_csv(file)
    
    if "text" not in df.columns:
        return jsonify({"error": "CSV must contain a 'text' column"}), 400

    texts = df["text"].astype(str)
    preds = model.predict(texts)
    probs = model.predict_proba(texts)

    results = []
    for text, pred, prob in zip(texts, preds, probs):
        results.append({
            "text": text,
            "prediction": "Ham" if pred == 1 else "Spam",
            "probability_spam": round(float(prob[0]), 3),
            "probability_ham": round(float(prob[1]), 3)
        })

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
