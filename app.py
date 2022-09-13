import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import pandas as pd
import numpy as np
import json

app = Flask(__name__)
#load the model
regmodel = pickle.load(open("car_price.pkl","rb"))
 
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict_api',methods = ['POST'])

def predict_api():
    data = request.json['data']
    y = json.dumps(data)
    z = json.loads(y)
    ls = [z["Present_Price"],z["Kms_Driven"],z["Owner"],z["total_years"],
	  z["Fuel_Type_Diesel"],z["Fuel_Type_Petrol"],z["Seller_Type_Individual"],
      z["Transmission_Manual"]]
    output = regmodel.predict([ls])
    print(output[0])
    return jsonify(output[0])

if __name__=="__main__":
    app.run(debug = True)
