# -*- coding:utf-8 -*-

import os
import joblib
import datetime

from multiprocessing import cpu_count
from functools import partial

from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.cluster import MiniBatchKMeans
from bayes_opt import BayesianOptimization


class MiniBatchKmeans:
    def __init__(self, conf=None):
        self.conf = conf
    
        self.s_score = 0
        self.best_model = None
        
    def silhouette_coeff_score(self, data, label):
        return silhouette_score(data, label)
    
    def mini_batch_kmeans(self,root_path, n_clusters, max_iter):
        kmeans = MiniBatchKMeans(
            n_clusters=int(n_clusters),
            max_iter=int(max_iter),
            batch_size = int(256*cpu_count()*0.8), 
        )
        
        kmeans.fit(self.train_data)
        
        _, xtest, _, ytest = train_test_split( # for big train_data
            self.train_data, 
            kmeans.predict(self.train_data), 
            test_size=0.15, 
            shuffle=True
            )
        scs = self.silhouette_coeff_score(xtest, ytest)
        if scs > self.s_score:
            self.best_model = kmeans

            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
            model_file = os.path.join(root_path, 
                                      'MiniBatchKMeans_{:.4}_{}.pkl'.format(scs, timestamp))
            joblib.dump(kmeans, model_file)

            print('silhouette_coeff: best {}, current {}'.format(self.s_score, scs))
            self.s_score = scs
            
        return scs
        
    def mini_batch_kmeans_init(self, train_data, test_data):
        self.s_score = 0
        
        self.train_data, self.test_data = train_data, test_data
    
    def get_params(self):
        return {
            'n_clusters': [2, 150],
            'max_iter': [100, 350],
        }
    
    def train(self, root_path, train_data, test_data, mini_batch_kmeans_params=None):
        self.mini_batch_kmeans_init(train_data, test_data)
        
        if mini_batch_kmeans_params is not None:
            pbounds = mini_batch_kmeans_params
        else:
            pbounds = self.get_params()
        
        print('MiniBatchKMeans_params:', pbounds)
        bo = BayesianOptimization(
                    f = partial(self.mini_batch_kmeans, root_path),
                    pbounds=pbounds,
                )
        bo.maximize(init_points=4, n_iter=9)

        s = self.silhouette_coeff_score(
            self.test_data, self.best_model.predict(self.test_data)
        )
        print('test_data: ', s)
