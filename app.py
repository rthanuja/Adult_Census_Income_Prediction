from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin
#import Flask_MonitoringDashboard as dashboard
import os

from src.IncomePrediction.validation_Insertion.training_validation_insertion import train_validation
from src.IncomePrediction.pipelines.training_pipeline import TrainModel
from src.IncomePrediction.pipelines.prediction_pipeline import Prediction
from src.IncomePrediction.validation_Insertion.prediction_validation_insertion import predict_validation
from src.IncomePrediction.logger import logging

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
#dashboard.bind(app)
#CORS(app)


@app.route("/",methods=['GET'])
#@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        filename = request.form['filename']  # Access filename from query parameters
        
            
        if filename is not None:
            path = filename
            logging.info(filename+"success")
            pred_val = predict_validation(path) #object initialization

            pred_val.predict_validation() #calling the prediction_validation function

            pred = Prediction(path) #object initialization

            # predicting for dataset present in database
            path = pred.PredictFromModel()
            return Response("Prediction File created at %s!!!" % path)
        '''elif request.form is not None:
            path = request.form['filepath']

            pred_val = predict_validation(path) #object initialization

            pred_val.predict_validation() #calling the prediction_validation function

            pred = Prediction(path) #object initialization


            # predicting for dataset present in database
            path = pred.PredictFromModel()
            return Response("Prediction File created at %s!!!" % path)'''
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['GET'])
#@cross_origin()
def trainRouteClient():

    try:

        filename = request.args.get('filename')  # Access filename from query parameters
        
            
        if filename is not None:
            path = filename
            logging.info(f"{path}")
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = TrainModel() #object initialization
            trainModelObj.train_model() #training the model for the files in the table"""


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

if __name__==  "__main__":
    app.run(host="127.0.0.1",port=8080,debug=True)