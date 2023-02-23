# -*- coding:utf-8 -*-

import os
import time
import warnings
warnings.filterwarnings('ignore')

import shap
import pandas as pd

from sklearn.model_selection import train_test_split

from setting import (drop_name_list,
                     y_label_list,
                     column_name_list,
                    )


def shap_gbm(parquet_file, model_file):
    feature_name =[]
    for i in column_name_list:
        if i not in drop_name_list and i not in y_label_list:
            feature_name.append(i)
    
    # load data
    data = pd.read_parquet(parquet_file)
    x = data[feature_name].astype('float')
    y = data[y_label_list]
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.15, shuffle=True)
    
    # load model
    model = joblib.load(model_file)
    
    explainer = shap.explainers.Permutation(model.predict_proba, X_train)
    shap_values = explainer(X_train[:100])
    
    # Plot a global summary
    shap.summary_plot(shap_values, X_train, feature_names=feature_name, plot_type="bar", max_display=50)
    
    # Plot a single instance
    shap.plots.waterfall(shap_values[1])


if __name__ == "__main__":
    parquet_file='/path/file_name.parquet'
    model_file = os.path.join('/root_path',
                          'tree_model_name.pkl',
                          )
    shap_gbm(parquet_file, model_file)
    
