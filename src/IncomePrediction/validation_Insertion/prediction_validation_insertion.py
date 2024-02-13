from src.IncomePrediction.validation_components.prediction_raw_validation import Prediction_Data_Validation
from src.IncomePrediction.validation_components.prediction_DB_operation import DBOperation
from src.IncomePrediction.validation_components.prediction_data_transform import DataTransformPrediction
from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException

import sys

class predict_validation:

    "This class is used to validate the prediction raw data"
    def __init__(self,path):
        self.raw_data = Prediction_Data_Validation(path)
        self.DBOperation = DBOperation()
        self.DataTransform = DataTransformPrediction()

    def predict_validation(self):

        try:
            LengthOfDateStampInFile,LengthOfTimeStampInFile,NumberofColumns,ColumnNames = self.raw_data.ValuesFromSchema()
            self.raw_data.FileNameValidation(LengthOfDateStampInFile,LengthOfTimeStampInFile)
            self.raw_data.ColumnLengthValidation(NumberofColumns)
            self.raw_data.ValidateMissingValuesinWholeColumn()
            self.DataTransform.DataFormatForSql()
            self.DBOperation.DatabaseConnection(DatabaseName='Prediction')
            self.DBOperation.CreateTableDb('Prediction',ColumnNames)
            self.DBOperation.InsertGoodDataToTable('Prediction')
            self.raw_data.DeleteExistingTrainingGoodRawDataFolder()
            self.raw_data.MoveBadDataToArchiveData()
            self.raw_data.DeleteExistingTrainingBadRawDataFolder()
            self.DBOperation.InputDataFromTableToCSV('Prediction')

        except Exception as e:
            logging.info("train_validation not successful")
            raise customException(e,sys)