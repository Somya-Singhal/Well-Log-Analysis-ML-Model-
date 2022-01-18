from flask import Flask,request
import pandas as pd
import numpy as np
import joblib
from joblib import dump, load
import flasgger
from flasgger import Swagger

# 2.CREATE THE APP OBJECT
app=Flask(__name__)

Swagger(app)
model = load('Random-Forest3.pkl')

@app.route('/')
def index():
    return  "PREDICTION USING RANDOM FOREST CLASSIFIER ON WELL LOG DATA"

# 4. EXPOSE THE PREDICTION FUNCTIONALITY, MAKE PREDICTION FROM PASSED JSON DATA AND RETURN THE PREDICTED VALUE
@app.route('/predict',methods=["Get"])
def predict_litho_level():
  """To Predict the Lithology level from well log data
#   This is using docstrings for specifications.
  ---
  parameters:
    - name: RHOB
      in: query
      type: number
      required: true
    - name: GR
      in: query
      type: number
      required: true
    - name: NPHI
      in: query
      type: number
      required: true
    - name: DTC
      in: query
      type: number
      required: true
    - name: DTS
      in: query
      type: number
      required: true

  responses:
       200:
           description: The output values   
  
  """

  RHOB=request.args.get('RHOB')
  GR=request.args.get('GR')
  NPHI=request.args.get('NPHI')
  DTC=request.args.get('DTC')
  DTS=request.args.get('DTS')

  prediction=model.predict([[RHOB,GR,NPHI,DTC,DTS]])
  lithoDic = {'Sandstone/Shale': (0,3),
            'Limestone': (3,6),
            'Anhydrite': (6,9),
            'Coal': (9,11)
  }

  pred=int(prediction)
  print(pred)
  for names, lithoDic in lithoDic.items():
      if(lithoDic[0]<=pred<lithoDic[1]):
          print(names)
          return "The Predicted Lithology Facies Value is: "+ str(pred)+" and Litho Facies type is: "+ names
          break


@app.route('/predict_file',methods=["POST"])
def predict_litho_level_file():
  """To Predict the Lithology level from well log data
#   This is using docstrings for specifications.
  ---
  parameters:
    - name: file
      in: formdata
      type: file
      required: true

  responses:
    200:
        description: The output values

  """

  wells=pd.read_csv(request.files.get("file"))
  print(wells.head())
  prediction=model.predict(wells)

  return "The predicted values for the csv file is:"+ str(list(prediction))


if __name__=='__main__':
  app.run()