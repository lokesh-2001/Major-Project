import pickle
from script.csvImport import *
from script.csvAppend import *
from flask import render_template, redirect, session
from datetime import datetime

data = import_csv("DhtDatalogger\dhtReading.csv")
output = import_csv("results.csv")
print(data)
print(output)
predictionData = data[-1]
outputData = []

if(len(output) != 0):
    outputData = output[-1]

appendToCsv = output[-1]
last_row = [[predictionData[1], predictionData[0]]]

model = pickle.load(open('./models/svm.pkl', 'rb'))

today = datetime.now()
date = today.strftime("%d/%m/%Y %H:%M:%S")
date = date.split(" ")
def home():
    if 'loggedin' in session:
        prediction = model.predict(last_row) 
        rain = "No"
        if(prediction[0] == 1):
            rain = "Yes"
        while(True):
            if(appendToCsv[-1] == "Yes" or appendToCsv[-1] == "No"):
                break                
            else:
                appendToCsv.insert(2, rain)
                break
        appendToCsv.insert(0, date[0])
        appendToCsv.insert(1, date[1])
        if(len(outputData) == 0):
            writeToCsv(appendToCsv)
        else:
            if(appendToCsv[2] != outputData[1] and appendToCsv[3] != outputData[0]):
                writeToCsv(appendToCsv)
        return render_template('index.html',
        prediction_text='Rain Today: {}'.format(rain),
        temperature=' {}'.format(predictionData[0]),
        humidity=' {}'.format(predictionData[1])) 
    return redirect('/login/')
