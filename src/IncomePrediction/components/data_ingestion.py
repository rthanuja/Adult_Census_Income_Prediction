from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException

import pandas as pd
import os
import sys

class Data_Ingestion:

    def __init__(self):
        self.training_file='Training_FileFromDB/InputFile.csv'

    def initiate_data_ingestion(self):
        logging.info("started initiation of data ingestion")
        try:
            data = pd.read_csv(os.path(self.training_file))
            logging.info("read data as dataframe and data ingestion completed")

        except Exception as e:
            logging.info("error occured at data ingestion stage")
            raise customException(e,sys)
