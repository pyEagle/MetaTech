# -*- coding:utf-8 -*-

import os
import joblib
import datetime
import multiprocessing

import lightgbm as lgb

from functools import partial

from sklearn import metrics
from numpy import argmax

from bayes_opt import BayesianOptimization


class TreeGbm:
    def __init__(self, root_path = './pkl'):
        self.root_path = root_path
        
        self.auc = 0
        self.mse = 1e6
        self.mape = 1e6
        self.tree_r2_score = 0
        self.acc = 0
        self.epsilon = 0.000001
        
        self.x_train, self.y_train, self.x_test, self.y_test = None, None, None, None
    
    @staticmethod
    def auc_score(y_true, y_pred_score):
        f, t, _ = metrics.roc_curve(y_true, y_pred_score, pos_label=1)
        return metrics.auc(f, t)
    
    @staticmethod
    def recall_precision_score(true_y, pred_y):
        recall = metrics.recall_score(true_y, pred_y)
        precision = metrics.precision_score(true_y, pred_y)
        return recall, precision
    
    @staticmethod
    def mse_score(y_true, y_pred):
        return metrics.mean_squared_error(y_true, y_pred)

    @staticmethod
    def mape_score(y_true, y_pred):
        return metrics.mean_absolute_percentage_error(y_true, y_pred).r2_score()
    
    @staticmethod
    def r2_score(y_true, y_pred):
        return metrics.r2_score(y_true, y_pred)
    
    @staticmethod
    def acc_score(y_true, y_pred):
        return metrics.accuracy_score(y_true, y_pred)
    
    @staticmethod
    def save_model(model, file_name):
        joblib.dump(model, file_name)
    
    def single_class_train(self, name, num_leaves, max_depth, learning_rate, n_estimators, min_child_samples, reg_alpha, reg_lambda):
        params = {
            'objective': 'binary',
            'num_leaves': int(num_leaves),
            'max_depth': int(max_depth),
            'learning_rate': learning_rate,
            'n_estimators': int(n_estimators),
            'min_child_samples': int(min_child_samples),
            'reg_alpha': reg_alpha,
            'reg_lambda': reg_lambda,
            'feature_pre_filter': False,
            'is_unbalance':True,
            'n_jobs': int(multiprocessing.cpu_count()*0.85),
            'verbose': -1,  
        }
        model = lgb.LGBMClassifier(**params)
        model.fit(
            self.x_train, 
            self.y_train,
            eval_set=[(self.x_test, self.y_test)],  
            early_stopping_rounds=25,
            verbose=False
        )
        
        y_pred = model.predict_proba(self.x_test)
        auc = self.auc_score(self.y_test, y_pred[:, 1])
        
        if auc > self.auc:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
            model_file = os.path.join(self.root_path, 
                                      'lightgbm_{}_{:.4}_{}.pkl'.format(name, auc, timestamp))
            self.save_model(model, model_file)
            
            print('auc', auc, params)
            self.auc = auc
        
        return auc
    
    def multi_class_train(self, name, num_leaves, max_depth, learning_rate, n_estimators, min_child_samples, reg_alpha, reg_lambda):
        params = {
            'objective': 'multiclass',
            'num_leaves': int(num_leaves),
            'max_depth': int(max_depth),
            'learning_rate': learning_rate,
            'n_estimators': int(n_estimators),
            'min_child_samples': int(min_child_samples),
            'reg_alpha': reg_alpha,
            'reg_lambda': reg_lambda,
            'num_class': self.num_class,
            'feature_pre_filter': False,
            'is_unbalance':True,
            'n_jobs': int(multiprocessing.cpu_count()*0.85),
            'verbose': -1,
            
        }
        model = lgb.LGBMClassifier(**params)
        model.fit(
            self.x_train, 
            self.y_train,
            eval_set=[(self.x_test, self.y_test)],  
            early_stopping_rounds=25,
            verbose=False
        )
        
        y_pred = model.predict(self.x_test)
        
        acc = self.acc_score(self.y_test, y_pred)
        
        if acc > self.acc:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
            model_file = os.path.join(self.root_path, 
                                      'lightgbm_{}_{:.4}_{}.pkl'.format(name, acc, timestamp))
            self.save_model(model, model_file)
            
            print('acc', acc, params)
            self.acc = acc

        return acc
    
    def regression_train(self, name, num_leaves, max_depth, learning_rate, n_estimators, min_child_samples, reg_alpha, reg_lambda):
        params = {
            'objective': 'regression',
            'num_leaves': int(num_leaves),
            'max_depth': int(max_depth),
            'learning_rate': learning_rate,
            'n_estimators': int(n_estimators),
            'min_child_samples': int(min_child_samples),
            'reg_alpha': reg_alpha,
            'reg_lambda': reg_lambda,
            'feature_pre_filter': False,
            'is_unbalance':True,
            'n_jobs': int(multiprocessing.cpu_count()*0.85),
            'verbose': -1,
            
        }
        model = lgb.LGBMRegressor(**params)
        model.fit(
            self.x_train, 
            self.y_train,
            eval_set=[(self.x_test, self.y_test)],  
            early_stopping_rounds=25,
            verbose=False
        )
        
        y_pred = model.predict(self.x_test)
        tree_r2_score = self.r2_score(self.y_test, y_pred)
        
        if tree_r2_score > self.tree_r2_score:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
            model_file = os.path.join(self.root_path, 
                                      'lightgbm_{}_{:.4}_{}.pkl'.format(name, tree_r2_score, timestamp))
            self.save_model(model, model_file)
            
            print('r2_score', tree_r2_score, params)
            self.tree_r2_score = tree_r2_score
        
        return tree_r2_score
    
    
    def get_params(self):
         return {
            'num_leaves': [5, 15] ,
            'max_depth': [3, 25],
            'learning_rate': [0.01, 0.55],
            'n_estimators': [5, 1800],
            'min_child_samples': [20, 100],
            'reg_alpha': [0.001, 0.95],
            'reg_lambda': [0.001, 0.95],
        }

    def set_trace_flag_init(self):
        self.auc = 0
        self.mse = 1e6
        self.mape = 1e6
        self.tree_r2_score = 0
        self.acc = 0
        self.epsilon = 0.000001
    
    def set_train_test_xy(self, x_train, y_train, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        
    def train(self, flag, name, x_train, y_train, x_test, y_test, num_class=5, tree_params=None):
        
        self.set_trace_flag_init()
        self.set_train_test_xy(x_train, y_train, x_test, y_test)
        
        if tree_params is None:
            pbounds = self.get_params()
        else:
            pbounds = tree_params
            
        if flag == 'single_class_train':           
            bo = BayesianOptimization(
                f = partial(self.single_class_train, name),
                pbounds=pbounds,
            )
            bo.maximize(init_points=4, n_iter=9)

        elif flag == 'multi_class_train':
            self.num_class = num_class
            bo = BayesianOptimization(
                f = partial(self.multi_class_train, name),
                pbounds=pbounds,
            )
            bo.maximize(init_points=4, n_iter=9)

        elif flag == 'regression':
            bo = BayesianOptimization(
                f = partial(self.regression_train, name),
                pbounds=pbounds,
            )
            bo.maximize(init_points=4, n_iter=9)

        else:
            raise ValueError('flag must be single_class_train, multi_class_train or regression!')
            
