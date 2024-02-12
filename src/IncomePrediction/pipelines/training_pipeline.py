from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException
from src.IncomePrediction.components.data_ingestion import Data_Ingestion
from src.IncomePrediction.components.data_transformation import DataTranformation
from src.IncomePrediction.components.best_model import Model_finder
from src.IncomePrediction.utils.file_methods import File_Operation

from sklearn.model_selection import train_test_split
import sys
import os
import pandas as pd

class TrainModel:
    
    def train_model(self):    
        logging.info("Start of Training!")  
        try:    
            data_ingestion_obj = Data_Ingestion()
            
            data = data_ingestion_obj.initiate_data_ingestion()

            data_tranformation_obj = DataTranformation()

            X= data_tranformation_obj.initialize_data_transformation(data)

            list_of_clusters = X['cluster'].unique()


            for i in list_of_clusters:
                cluster_data= X[X['cluster']==i] # filter the data for one cluster
                # Prepare the feature and Label columns
                cluster_features= cluster_data.drop(['Labels','cluster'],axis=1)
                cluster_label= cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=355)

                model_finder = Model_finder() # object initialization

                #getting the best model for each of the clusters
                
                best_model_name,best_model = model_finder.get_best_model(x_train,y_train,x_test,y_test)

                file_obj = File_Operation()
                filename = best_model_name+str(i)
                file_obj.save_model(file_path = os.path.join('artifacts',filename),
                                    obj = best_model)
                logging.info("successful end of training")

        except Exception as e:
            logging.info("error occcured in training pipeline")
            raise customException(e,sys)

    

