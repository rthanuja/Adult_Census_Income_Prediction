from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException
from os import listdir
import os
import sys
import pandas as pd

class DataTransformPrediction:
    """This class is used for transforming raw data before loading into database"""

    def __init__(self):
        self.GoodDataPath = "Prediction_Raw_Data_validated/Good_Raw"

    def DataFormatForSql(self):

        """This method is used to insert quotes to string data for loading into sql database"""
        
        logging.info("data transformation started for raw data to move to sql")
        try:
            filelist = [f for f in listdir(os.path.join(self.GoodDataPath))]
            for file in filelist:
                data = pd.read_csv(self.GoodDataPath + "/" + file)
                # list of columns with string datatype variables
                columns = [ 'workclass','education', 'marital-status', 'occupation', 'relationship',
                            'race','sex', 'native-country']
                for col in columns:
                    data[col] = data[col].apply(lambda x: "'" + str(x) + "'")
                data.to_csv(self.GoodDataPath + "/" + file, index=None, header=True)
                logging.info(f"Quotes added successfully for {file}")
            logging.info("data transformation finished")
        except Exception as e:
            logging.info("error occured while transforming data")
            raise customException(e,sys)
