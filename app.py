from flask import Flask, render_template, request
import requests

app = Flask(__name__)

history = []

# 🌍 TRANSLATION FUNCTION
def translate_text(text, dest):
    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": dest,
        "dt": "t",
        "q": text
    }

    response = requests.get(url, params=params)
    result = response.json()

    translated = result[0][0][0]
    detected = result[2]

    return translated, detected


@app.route("/", methods=["GET", "POST"])
def home():
    translated = ""
    detected = ""

    if request.method == "POST":
        text = request.form["text"]
        dest = request.form["dest"]

        translated, detected = translate_text(text, dest)

        history.append((text, translated))

    return render_template("index.html",
                           translated=translated,
                           detected=detected,
                           history=history)


if __name__ == "__main__":
    app.run(debug=True)
