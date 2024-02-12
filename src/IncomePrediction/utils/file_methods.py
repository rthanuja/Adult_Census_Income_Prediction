import os
import sys
import pickle

from src.IncomePrediction.exception import customException
from src.IncomePrediction.logger import logging

class File_Operation:
    def save_model(self,file_path, obj):
        try:
            logging.info('Entered the save_model method of the File_Operation class')
            dir_path = os.path.dirname(file_path)

            os.makedirs(dir_path, exist_ok=True)

            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)
            logging.info(f'Model File {obj} saved. Exited the save_model method of the file_operation class')

        except Exception as e:
            logging.info("error occured in save model method of file operation class")
            raise customException(e, sys)

    def load_model(self,file_path):
        try:
            logging.info('Entered the load_model method of the File_Operation class')
            with open(file_path,'rb') as file_obj:
                logging.info(f'Model File {file_obj} loaded. Exited the load_model method of the file_operation class')
                return pickle.load(file_obj)
            
        except Exception as e:
            logging.info('Exception Occured in load_model method of file operation class')
            raise customException(e,sys)

