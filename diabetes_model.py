# model for the diabetes


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier


def sugar_prediction_patient(fname):
    data = pd.read_csv('diabetes_csv.csv')
    real_x = data.iloc[:,[i for i in range(0, 8)]].values
    real_y = data.iloc[:,8].values
    working_data = pd.read_csv(fname)
    working_x = working_data.iloc[:,[i for i in range(1, 9)]].values
    training_x,test_x,training_y,test_y = train_test_split(real_x, real_y, test_size = 0.25, random_state = 0)
    s_c = StandardScaler()
    training_x = s_c.fit_transform(training_x)
    working_x = s_c.fit_transform(working_x)
    cls = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
    cls.fit(training_x, training_y)
    working_y = cls.predict(working_x)
    print(working_y)
    return working_y

if __name__ == '__main__':
    result_list = sugar_prediction_patient('sugar_test.csv')
    print(result_list)
