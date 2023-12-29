from flask import Flask, render_template, request, jsonify

from chat import get_response

app = Flask(__name__)

#define 2 routes for the webpage - a home and a predict
@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # @Todo: check if text is valid, and other error checks
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__=="__main__":
    app.run(debug=True)