from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,roc_auc_score,classification_report

import sys

class Model_finder:

    """This model is used to find model with best accuracy and auc score"""

    def __init__(self):
        self.lg = LogisticRegression()
        self.gnb = GaussianNB()
        self.svc = SVC()
        self.rf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic',n_jobs=-1)


    def get_best_params_for_random_forest(self,x_train,y_train):
        logging.info("Entered the get_best_params_for_random_forest method of the Model_Finder class")
        try:
            # initializing with different combination of parameters
            self.param_grid = { "n_estimators": [50,100], "criterion": ['gini', 'entropy'],"max_depth": [6,7,8]}
            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.rf, param_grid=self.param_grid, cv=5,  verbose=3)
            #finding the best parameters
            self.grid.fit(x_train, y_train)
            #extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']
            #creating a new model with the best parameters
            self.rf = RandomForestClassifier(criterion=self.criterion, max_depth=self.max_depth,n_estimators= self.n_estimators, n_jobs=-1)
            # training the mew model
            self.rf.fit(x_train, y_train)
            logging.info(f"random forest best params: {self.grid.best_params_}. Exited the get_best_params_for_random_forest method of the Model_Finder class")
            return self.rf
        
        except Exception as e:
            logging.info(f"Error occured in get_best_params_for_random_forest method of the Model_Finder class.Error message:{e}")
            logging.info('random forest Parameter tuning  failed. Exited the get_best_params_for_random_forest of the Model_Finder class')
            raise customException(e,sys)



    def get_best_params_for_naive_bayes(self,x_train,y_train):
        logging.info("Entered the get_best_params_for_naive_bayes method of the Model_Finder class")
        try:
            # initializing with different combination of parameters
            self.param_grid = {"var_smoothing": [1e-9,0.1, 0.001, 0.5,0.05,0.01,1e-8,1e-7,1e-6,1e-10,1e-11]}
            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.gnb, param_grid=self.param_grid, cv=5,  verbose=3)
            #finding the best parameters
            self.grid.fit(x_train, y_train)
            #extracting the best parameters
            self.var_smoothing = self.grid.best_params_['var_smoothing']
            #creating a new model with the best parameters
            self.gnb = GaussianNB(var_smoothing=self.var_smoothing)
            # training the mew model
            self.gnb.fit(x_train, y_train)
            logging.info(f"Naive Bayes best params: {self.grid.best_params_}. Exited the get_best_params_for_naive_bayes method of the Model_Finder class")
            return self.gnb
        
        except Exception as e:
            logging.info(f"Error occured in get_best_params_for_naive_bayes method of the Model_Finder class.Error message:{e}")
            logging.info('naive bayes Parameter tuning  failed. Exited the get_best_params_for_naive_bayes method of the Model_Finder class')
            raise customException(e,sys)



    def get_best_params_for_xgboost(self,x_train,y_train):
        logging.info("Entered the get_best_params_for_xgboost method of the Model_Finder class")
        try:
            # initializing with different combination of parameters
            self.param_grid_xgboost = {"n_estimators": [80,100],"max_depth": range(7, 9, 1),'learning_rate': [0.01, 0.1] }
            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(estimator=self.xgb,param_grid=self.param_grid_xgboost, verbose=3,cv=5)
            # finding the best parameters
            self.grid.fit(x_train, y_train)

            # extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(objective='binary:logistic',learning_rate=self.learning_rate, max_depth=self.max_depth,n_estimators= self.n_estimators, n_jobs=-1 )
            # training the mew model
            self.xgb.fit(x_train, y_train)
            logging.info(f"XGBoost best params: {self.grid.best_params_}. Exited the get_best_params_for_xgboost method of the Model_Finder class")
            return self.xgb
        
        except Exception as e:
            logging.info(f"Error occured in get_best_params_for_xgboost method of the Model_Finder class.Error message: {e}")
            logging.info('XGBoost Parameter tuning  failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise customException(e,sys)
            
    def get_best_model(self,x_train,y_train,x_test,y_test):
        model ={}
        accuracy = {}
        try:
            # create best model for xgboost
            self.xgboost= self.get_best_params_for_xgboost(x_train,y_train)
            self.prediction_xgboost = self.xgboost.predict(x_test) # Predictions using the XGBoost Model

            if len(y_test.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.xgboost_score = accuracy_score(y_test, self.prediction_xgboost)
                logging.info(f"Accuracy for XGBoost: {self.xgboost_score}")  # Log AUC
            else:
                self.xgboost_score = roc_auc_score(y_test, self.prediction_xgboost) # AUC for XGBoost
                logging.info(f"AUC for XGBoost: {self.xgboost_score}") # Log AUC
            model['XGBoost'] = self.xgboost
            accuracy['XGBoost'] =self.xgboost_score

            # create best model for Random Forest
            self.random_forest= self.get_best_params_for_random_forest(x_train,y_train)
            self.prediction_random_forest = self.random_forest.predict(x_test) # Predictions using the XGBoost Model

            if len(y_test.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(y_test, self.prediction_random_forest)
                logging.info(f"Accuracy for RandomForest: {self.random_forest_score}")  # Log AUC
            else:
                self.random_forest_score = roc_auc_score(y_test, self.prediction_random_forest) # AUC for XGBoost
                logging.info(f"AUC for RandomForest: {self.random_forest_score}") # Log AUC
            model['RandomForest'] = self.random_forest
            accuracy['RandomForest'] =self.random_forest_score

            # create best model for naive bayes
            self.naive_bayes=self.get_best_params_for_naive_bayes(x_train,y_train)
            self.prediction_naive_bayes=self.naive_bayes.predict(x_test) # prediction using the naive bayes Algorithm

            if len(y_test.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.naive_bayes_score = accuracy_score(y_test,self.prediction_naive_bayes)
                logging.info(f"Accuracy for NB: {self.naive_bayes_score}")
            else:
                self.naive_bayes_score = roc_auc_score(y_test, self.prediction_naive_bayes) # AUC for naive bayes
                logging.info(f"AUC for NB: {self.naive_bayes_score}")
            model['GaussianNB'] = self.naive_bayes
            accuracy['GaussianNB'] =self.naive_bayes_score

            # create best model for logistic regression
            self.lg.fit(x_train,y_train)
            self.prediction_logistic_reg=self.lg.predict(x_test) # prediction using the logistic regression Algorithm

            if len(y_test.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.logistic_reg_score = accuracy_score(y_test,self.prediction_logistic_reg)
                logging.info(f"Accuracy for LogisticRegression: {self.logistic_reg_score}")
            else:
                self.logistic_reg_score = roc_auc_score(y_test, self.prediction_logistic_reg) # AUC for naive bayes
                logging.info(f"AUC for LogisticRegression: {self.logistic_reg_score}")
            model['LogisticRegression'] = self.lg
            accuracy['LogisticRegression'] =self.logistic_reg_score

            # create best model for svc
            self.svc.fit(x_train,y_train)
            self.prediction_svc =self.svc.predict(x_test) # prediction using the logistic regression Algorithm

            if len(y_test.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.svc_score = accuracy_score(y_test,self.prediction_svc)
                logging.info(f"Accuracy for svc: {self.svc_score}")
            else:
                self.svc_score = roc_auc_score(y_test, self.prediction_svc) # AUC for naive bayes
                logging.info(f"AUC for svc: {self.svc_score}")
            model['SVC'] = self.svc
            accuracy['SVC'] =self.svc_score

            best_model_name = max(accuracy, key=accuracy.get)
            best_model = model[best_model_name]

            logging.info(f"The best model is: {best_model_name} with accuracy: {accuracy[best_model_name]} and exiting get_best_model")
            
            return best_model_name,best_model
        

        except Exception as e:
            logging.info("error occured at get_best_model of Model_finder class")
            raise customException(e,sys)




