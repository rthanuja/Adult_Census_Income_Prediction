from src.IncomePrediction.components.data_ingestion_prediction import Data_Ingestion_Prediction
from src.IncomePrediction.validation_components.prediction_raw_validation import Prediction_Data_Validation
from src.IncomePrediction.components.data_transformation import DataTranformation
from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException
from src.IncomePrediction.utils.file_methods import File_Operation

import sys
import os
import numpy as np
import pandas as pd

class Prediction:
    def __init__(self,path):
        self.pred_raw_val = Prediction_Data_Validation(path)
        self.data_tranform_obj = DataTranformation()

    def PredictFromModel(self):
        try:
            logging.info("Prediction started")
            self.pred_raw_val.deletePredictionFile()
            logging.info("deleted prediction file if exists")
            data_ingestion_obj = Data_Ingestion_Prediction()
            data = data_ingestion_obj.initiate_data_ingestion_prediction()
            data.replace('?', np.NaN,inplace=True)
            logging.info("? replaced with NaN")
            data.drop(columns='education',inplace=True)
            logging.info(f"dropped education column")
            self.data_tranform_obj.reduce_categories(data)
            preprocessor = self.data_tranform_obj.get_data_tranformation()
            arr = preprocessor.fit_transform(data)
            cols = preprocessor.get_feature_names_out(data.columns)
            data = pd.DataFrame(arr,columns=cols)
            cols = ','.join(data.columns.tolist())
            cols= cols.replace("num_pipeline__","",).replace("cat_pipeline__","")
            data.columns=cols.split(",")

            file_loader = File_Operation()
            kmeans = file_loader.load_model(os.path.join('artifacts','KMeans.sav'))

            clusters =kmeans.predict(data)
            data['cluster'] = clusters

            list_of_clusters = data['cluster'].unique()
            predictions = []

            for i in list_of_clusters:
                cluster_data= data[data['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                filepath = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(filepath)#correct filepath
                result=(model.predict(cluster_data))
                for res in result:
                    if res==0:
                        predictions.append('<=50K')
                    else:
                        predictions.append('>50K')

            final= pd.DataFrame(list(zip(predictions)),columns=['Predictions'])
            path="Prediction_Output_File/Predictions.csv"
            final.to_csv(os.path.join(path),header=True,mode='a+')
            logging.info("end of prediction")

        except Exception as e:
            logging.info(f"{e}: error occured while prediction")
            raise customException(e,sys)

        return path