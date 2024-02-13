from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException

import pandas as pd
import os
import sys

class Data_Ingestion_Prediction:

    def __init__(self):
        self.prediction_file='Prediction_FileFromDB/InputFile.csv'

    def initiate_data_ingestion_prediction(self):
        logging.info("started initiation of data ingestion")
        try:
            data = pd.read_csv(os.path.join(self.prediction_file),skipinitialspace=True)
            data = data.applymap(lambda x:x.strip() if isinstance(x,str) else x)

            logging.info("read data as dataframe and data ingestion completed")
            return data

        except Exception as e:
            logging.info("error occured at data ingestion stage")
            raise customException(e,sys)
        