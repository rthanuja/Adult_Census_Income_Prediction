from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException

import json
import os
import sys
import re
import pandas as pd
import shutil
from datetime import datetime


class Training_Data_Validation_Config:
    Good_raw_training_path = os.path.join("Training_Raw_Data_validated/","Good_Raw/")
    Bad_raw_training_path = os.path.join("Training_Raw_Data_validated/","Bad_Raw/")
    Bad_archive_data_path = os.path.join("Training_Archived_Bad_Data")



class Training_Data_Validation:
    """This class takes the input as path of training batch files and gives validated """
    def __init__(self,path):
        self.batch_directory = path
        self.schema_path = 'schema_training.json'
        self.validation_config = Training_Data_Validation_Config()

    def ValuesFromSchema(self):
        """This method gets the predefined schema details from json file object"""
        logging.info("training raw data validation started")
        try:
            with open(self.schema_path,'r') as fdata:
                dic = json.load(fdata)
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            NumberofColumns = dic['NumberofColumns']
            ColumnNames = dic['ColName']

            logging.info("values from schema extracted successfully!")

            return LengthOfDateStampInFile,LengthOfTimeStampInFile,NumberofColumns,ColumnNames

        except Exception as e:
            logging.info(f"{type(e).__name__}: ocurred while extracting values from schema") 
            raise customException(e,sys)
        
    
    def CreateDirectoryForGoodBadRawData(self):
        """This method creates a directory for creating directory for good and bad raw data validated"""
        logging.info("creating directory for good and bad data")
        try:
            os.makedirs(os.path.dirname(os.path.join(self.validation_config.Good_raw_training_path)),exist_ok=True)
            os.makedirs(os.path.dirname(os.path.join(self.validation_config.Bad_raw_training_path)),exist_ok=True)

        except Exception as e:
            logging.info(f"{type(e).__name__} error occured while creating directory for good and bad raw data validated")
            raise customException(e,sys)

    def DeleteExistingTrainingGoodRawDataFolder(self):
        """This method deletes the directory of the good raw folder"""
        logging.info("deleting good raw data directory")
        try:
            path = "Training_Raw_Data_validated/"
            if os.path.isdir(path+'Good_Raw/'):
                shutil.rmtree(path+'Good_Raw/')
                logging.info("Good_raw directory removed successfully!")

        except Exception as e:
            logging.info(f"{type(e).__name__} error occured while deleting good_raw data directory")
            raise customException(e,sys)
        
    def DeleteExistingTrainingBadRawDataFolder(self):
        """This method deletes the directory of the bad raw folder"""
        logging.info("deleting bad raw data directory")
        try:
            path = "Training_Raw_Data_validated/"
            if os.path.isdir(path+'Bad_Raw/'):
                shutil.rmtree(path+'Bad_Raw/')
                logging.info("Bad_raw directory removed successfully!")

        except Exception as e:
            logging.info(f"{type(e).__name__} error occured while deleting bad_raw data directory")
            raise customException(e,sys)
        
    def MoveBadDataToArchiveData(self):
        """This method moves the bad_raw data to archive data"""
        logging.info("started moving bad raw data to archive bad data folder")
        now = datetime.now()
        date = now.date()
        time = now.strftime('%H%M%S')
        try:
            source = self.validation_config.Bad_raw_training_path
            if os.path.isdir(source):
                os.makedirs(os.path.dirname(os.path.join(self.validation_config.Bad_archive_data_path)),exist_ok=True)
                desti =  'Training_Archived_Bad_Data/BadData_' + str(date)+"_"+str(time)
                os.makedirs(desti,exist_ok=True)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(desti):
                        shutil.move(source+f,desti)
                logging.info("bad data moved to archive bad data folder")
        
        except Exception as e:
            logging.info("error while moving bada data to archive bad data folder")
            raise customException(e,sys)
        

    def FileNameValidation(self,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """This method validates the filename as per predefined schema.If it is not matched moved to bad raw data folder
        else moved to good raw folder"""
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.DeleteExistingTrainingBadRawDataFolder()
        self.DeleteExistingTrainingGoodRawDataFolder()
        #create new directories
        self.CreateDirectoryForGoodBadRawData()
        regex='incomeData_\d+_\d+\.csv'
        logging.info("filename validation started")
        try:
            onlyfiles = [f for f in os.listdir(self.batch_directory)]
            for filename in onlyfiles:
                if re.match(regex,filename):
                    SplitAtDot = filename.split(".csv")
                    SplitAtUnderScore = SplitAtDot[0].split("_")
                    if SplitAtUnderScore[1] == LengthOfDateStampInFile:
                        if SplitAtUnderScore[2] == LengthOfTimeStampInFile:
                            shutil.copy("Training_Batch_Files/" + filename, self.validation_config.Good_raw_training_path)
                            logging(f"Valid File Name!! File moved to Good Raw Folder :: { filename}")
                        else:
                            shutil.copy("Training_Batch_Files/" + filename, self.validation_config.Bad_raw_training_path)
                            logging(f"Invalid File Name!! File moved to Bad Raw Folder :: { filename}")

                    else:
                        shutil.copy("Training_Batch_Files/" + filename, self.validation_config.Bad_raw_training_path)
                        logging(f"Invalid File Name!! File moved to Bad Raw Folder :: { filename}")
                else:
                    shutil.copy("Training_Batch_Files/" + filename, self.validation_config.Bad_raw_training_path)
                    logging(f"Invalid File Name!! File moved to Bad Raw Folder :: { filename}")
            logging.info("filename validation completed")
        except Exception as e:
            logging.info("Error occured while validating filename")
            raise customException(e,sys)
        

    def ColumnLengthValidation(self,NumberofColumns):
        """This method validates the no of columns as per predefined schema.If it is not matched moved to bad raw data folder
        else moved to good raw folder"""
        logging.info("column length validation started")
        try:
            for file in os.listdir(self.validation_config.Good_raw_training_path):
                csv = pd.read_csv(os.path.join(self.validation_config.Good_raw_training_path+file))
                if csv.shape[1] == NumberofColumns:
                    pass
                else:
                    shutil.move("Training_Raw_files_validated/Good_Raw/" + file, self.validation_config.Bad_raw_training_path)
                    logging(f"Invalid Column length for File!! File moved to Bad Raw Folder :: { filename}")
            logging.info("column length validation completed")

        except Exception as e:
            logging.info(f"{type(e).__name__}:Error occured while validating column length")
            raise customException(e,sys)
        
    
    def ValidateMissingValuesinWholeColumn(self):
        """This method validates if any column in the csv file has all values missing and if missing moves to bad raw folder"""
        logging.info("started validating missing values in whole column")
        try:
            for file in os.listdir(self.validation_config.Good_raw_training_path):
                csv = pd.read_csv(os.path.join(self.validation_config.Good_raw_training_path+file))
                for col in csv:
                    if csv[col].count() == 0:
                        shutil.move("Training_Raw_files_validated/Good_Raw/" + file, self.validation_config.Bad_raw_training_path)
                        logging(f"Missing values in whole Column in the File!! File moved to Bad Raw Folder :: { filename}")
                        break
            logging.info("validation of missing values in whole column completed")
        except Exception as e:
            logging.info(f"{type(e).__name__}:Error occured while validating missing values in whole column")
            raise customException(e,sys)