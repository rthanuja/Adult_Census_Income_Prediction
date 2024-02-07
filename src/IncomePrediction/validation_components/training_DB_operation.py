from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException
from os import listdir
import csv
import sqlite3
import sys
import os
import shutil

   

class DBOperation:

    """This class is for handling all sql operations"""

    def __init__(self):
        self.path = 'Training_Database/'
        self.goodfilepath = "Training_Raw_Data_validated/Good_Raw"
        self.badfilepath = "Training_Raw_Data_validated/Bad_Raw"

    def DatabaseConnection(self,DatabaseName):

        """This method is used to create a database with a given name if already exists opens the connection to db"""

        logging.info("connection to database started")
        try:        
            conn = sqlite3.connect(self.path+DatabaseName+'.db')
            logging.info("connection completed")
            return conn
        
        except Exception as e:
            logging.info("error while connecting to database")
            raise customException(e,sys)
        
    def CreateTableDb(self,DatabaseName,col_names):

        """This method creates a table in the given database and inserts the good data after raw data validation"""

        logging.info("creating a table in the database started")
        try:
            conn = self.DatabaseConnection(DatabaseName)
            cursor = conn.cursor()
            cursor.execute("select count(name) from sqlite_master where type = 'table' and name='Good_Raw_Data'")
            if cursor.fetchone()[0]==1:
                conn.close()
                logging.info("table name already exists")
            else:
                for key in col_names.keys():
                    type = col_names[key]
                    try:
                        cursor.execute('Alter table good_raw_data add "{column_name}" {data_type}'.format(column_name=key,datatype=type))
                        logging.info(f"added {key} to table successfully")
                    except:
                        cursor.execute('create table if not exists good_raw_data ({column_name} {data_type})'.format(column_name=key,data_type=type))
                        logging.info(f"created table with {key} successfully")
                conn.close()
            logging.info("creating table in db completed")

        except Exception as e:
            logging.info(f"{type(e).__name__ }: error while creating a table in the database")
            raise customException(e,sys)
        
    def InsertGoodDataToTable(self,DatabaseName):

        """This method inserts the values from data files in the good raw data folder into table in the database """

        logging.info("inserting raw data into the good raw data table")

        conn = self.DatabaseConnection(DatabaseName)
        GoodFilePath = self.goodfilepath
        BadFilePath = self.badfilepath
        onlyfiles = [f for f in listdir(self.goodfilepath)]
        for file in onlyfiles:
            try:
                with open(GoodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f,delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in line[1]:
                            try:
                                conn.execute("insert into good_raw_data values ({values})".format(values=list_))
                                conn.commit()
                            except Exception as e:
                                logging.info(f"{type(e).__name__} error occured at {line[0]} in {file}")
                                raise customException(e,sys)
                logging.info("inserting data to able completed")

            except Exception as e:
                conn.rollback()
                logging.info(f"error occured in {file} while inserting data")
                shutil.move(GoodFilePath+'/' + file, BadFilePath)
                logging.info(f"moved {file} into bad raw folder")
                conn.close()

        conn.close()

    
    def InputDataFromTableToCSV(self,DatabaseName):

        """This method exports the good data to a csv file"""

        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        logging.info("Exporting data from table to csv file started")
        try:
            conn = self.DatabaseConnection(DatabaseName)
            query = "SELECT * FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(query)

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            os.makedirs(self.fileFromDb,exist_ok=True)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            logging.info("File exported successfully")

        except Exception as e:
            logging.info("error occured while exporting data to csv")
            raise customException(e,sys)

        conn.close()
