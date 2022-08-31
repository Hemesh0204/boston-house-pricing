import pickle

from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('regression.pkl', 'rb'))
scaler = pickle.load(open('scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods = ['post'])
def predict_api():
    data = request.json['data']
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output = model.predict(new_data)
    print(output)
    return jsonify(output)

@app.route('/predict', methods = ['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    final_op = scaler.transform(np.array(data).reshape(1, -1))
    print(final_op)
    op = model.predict(final_op)[0]
    return render_template('home.html', prediction_text = "The House price prediction is {}".format(op))

if __name__ == "__main__":
    app.run(debug=True)