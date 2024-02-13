from src.IncomePrediction.validation_components.training_raw_validation import Training_Data_Validation
from src.IncomePrediction.validation_components.training_DB_operation import DBOperation
from src.IncomePrediction.validation_components.training_data_transform import DataTransform
from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException

import sys

class train_validation:

    "This class is used to validate the training raw data"
    def __init__(self,path):
        self.raw_data = Training_Data_Validation(path)
        self.DBOperation = DBOperation()
        self.DataTransform = DataTransform()

    def train_validation(self):
        try:
            LengthOfDateStampInFile,LengthOfTimeStampInFile,NumberofColumns,ColumnNames = self.raw_data.ValuesFromSchema()
            self.raw_data.FileNameValidation(LengthOfDateStampInFile,LengthOfTimeStampInFile)
            self.raw_data.ColumnLengthValidation(NumberofColumns)
            self.raw_data.ValidateMissingValuesinWholeColumn()
            self.DataTransform.DataFormatForSql()
            self.DBOperation.DatabaseConnection(DatabaseName='Training')
            self.DBOperation.CreateTableDb('Training',ColumnNames)
            self.DBOperation.InsertGoodDataToTable('Training')
            self.raw_data.DeleteExistingTrainingGoodRawDataFolder()
            self.raw_data.MoveBadDataToArchiveData()
            self.raw_data.DeleteExistingTrainingBadRawDataFolder()
            self.DBOperation.InputDataFromTableToCSV('Training')

        except Exception as e:
            logging.info("train_validation not successful")
            raise customException(e,sys)

