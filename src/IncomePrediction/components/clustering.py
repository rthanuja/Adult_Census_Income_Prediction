from src.IncomePrediction.logger import logging
from src.IncomePrediction.exception import customException

from sklearn.cluster import KMeans
from kneed import KneeLocator
import matplotlib.pyplot as  plt
import sys


class KMeansClustering:
    
    """This class is used for creating clusters in the given data before training"""

    def elbow_plot(self,data):

        """This method saves the elbow plot to decide optimum no of clusters"""

        logging.info("entered elbow method of kmeans clustering")
        try:
            wcss = []
            for i in range(1,11):
                kmeans = KMeans(n_clusters=i,init='k-means++',random_state=42)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11),wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            self.kn = KneeLocator(x=range(1,11),y=wcss,curve='convex',direction='decreasing')
            logging.info(f"optimum number of clusters : {self.kn.knee}")
            return self.kn.knee
        
        except Exception as e:
            logging.info("error occured in elbow plot method of kmeans clustering")
            raise customException(e,sys)
        
    def create_clusters(self,data,NumberOfClusters):

        """This method creates a new dataframe with cluster information"""
        
        logging.info("entered the createclusters of kmeans clustering")
        try:
            kmeans = KMeans(n_clusters=NumberOfClusters,init='k-means++',random_state=42)
            cluster = kmeans.fit_predict(data)
            data["cluster"] = cluster
            logging.info(f"successfully created {self.kn.knee} clusters.exited create clusters method")
        
        except Exception as e:
            logging.info("error occured ehile creating clusters")
            raise customException(e,sys)

