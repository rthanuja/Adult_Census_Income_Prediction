from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException
from src.IncomePrediction.components.clustering import KMeansClustering

from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import RandomOverSampler

import numpy as np
import pandas as pd
import sys


class DataTranformation:

    def get_data_tranformation(self):

        """This method returns the preprocessor object from the pipeline"""

        try:
            logging.info("Data Transformation initiated")

            #define which columns shpuld be ordinally encoded and which should be scaled
            categorical_cols = ['workclass', 'marital-status', 'occupation','relationship', 'race', 'sex', 'native-country']
            numerical_cols = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss','hours-per-week']
            
            #numerical pipeline
            num_pipeline = Pipeline( steps=[  ('imputer',SimpleImputer(strategy='median')),
                                            ('scaler',StandardScaler())
                                        ]
                                )

            #categorical pipeline
            cat_pipeline = Pipeline(
                        steps=[

                            ('imputer',SimpleImputer(strategy='most_frequent')),
                            ('onehotcoder',OneHotEncoder(sparse_output=False,drop='first'))
                        ]
                    )
                                    
            preprocessor = ColumnTransformer(
                        transformers=        
                        [
                            ('num_pipeline',num_pipeline,numerical_cols),
                            ('cat_pipeline',cat_pipeline,categorical_cols)
                        ]
                    )
            logging.info("preprocessing pipeline completed successfully")
            return preprocessor
            

        except Exception as e:
            logging.info("Exception occured in the get_data_transformation")

            raise customException(e,sys)
        
    def reduce_categories(self,data):

        """This method is used to combine data logically to reduce categories"""
        try:
            logging.info("entered reduce categories method of data transformation")
            replacement_dict = {**dict.fromkeys([1,2,3,4,5,6,7,8],1),**dict.fromkeys([9,10],2),**dict.fromkeys([11,12],3),
                    **dict.fromkeys([13],4),**dict.fromkeys([14],5),**dict.fromkeys([15,16],6)}
            data['education-num'].replace(replacement_dict,inplace=True)
            workclass_replace= {**dict.fromkeys([ 'Never-worked'],'Without-pay'),**dict.fromkeys(['Self-emp-not-inc'],'Private'),
                    **dict.fromkeys(['State-gov','Local-gov'],'gov')}
            data['workclass'].replace(workclass_replace,inplace=True)
            data['relationship'].replace(['Not-in-family', 'Own-child', 'Unmarried','Other-relative'],'others',inplace=True)
            data['marital-status'].replace(['Divorced','Married-spouse-absent', 'Separated', 'Married-AF-spouse','Widowed'],'No-spouse',inplace=True)
            data['race'].replace('Amer-Indian-Eskimo','Other',inplace=True)
            logging.info("categories reduced succesfully")
            return data

        except Exception as e:
            logging.info("error occured while reducing categories of data in data transformation")
            raise customException(e,sys)
        

    def initialize_data_transformation(self,data):
        try:
            data.replace('?', np.NaN,inplace=True)
            data.drop(columns='education',inplace=True)
            data = self.reduce_categories(data)
            X = data.drop(columns='Income')
            Y = data['Income']
            Y = Y.map({'<=50K': 0, '>50K': 1})
            preprocessor = self.get_data_tranformation()
            arr = preprocessor.fit_transform(X)
            cols = preprocessor.get_feature_names_out(X.columns)
            X = pd.DataFrame(arr,columns=cols)
            cols = ','.join(X.columns.tolist())
            cols= cols.replace("num_pipeline__","",).replace("cat_pipeline__","")
            X.columns=cols.split(",")
            randomsampler = RandomOverSampler()
            X,Y = randomsampler.fit_resample(X,Y)

            kmeans = KMeansClustering()
            Number_of_Clusters = kmeans.elbow_plot(X)
            X = kmeans.create_clusters(X,Number_of_Clusters)
            X['Labels'] = Y

            logging.info("preprocessing done succesfully")
            return X
        
        except Exception as e:
            logging.info("error occured while initializing data transformation")            
            raise customException(e,sys)


