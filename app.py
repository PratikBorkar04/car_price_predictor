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

@app.route('/predict',methods=['POST'])
def predict():
    
    Year = int(request.form['Year'])

    Present_Price=float(request.form['Present_Price'])

    Kms_Driven=int(request.form['Kms_Driven'])
    Owner=int(request.form['Owner'])
    Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']

    if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1

    Year=2022-Year

    Seller_Type_Individual=request.form['Seller_Type_Individual']
    if(Seller_Type_Individual=='Individual'):
                Seller_Type_Individual=1
                Seller_Type_Individual=0
    else:
        Seller_Type_Individual=0
        Seller_Type_Individual=1	

    Transmission_Mannual=request.form['Transmission_Mannual']
    if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
    else:
        Transmission_Mannual=0
    
    prediction=regmodel.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
    print([Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual])
    selling_price = ('%.2f' % prediction[0])
    return render_template("home.html",prediction_text="The car price is (in Lakhs) :- {}".format(selling_price))

if __name__=="__main__":
    app.run(debug = True)
