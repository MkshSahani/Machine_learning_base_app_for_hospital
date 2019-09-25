# model for the heart diseases.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier


def heart_prediction_patient(fname):

    data = pd.read_csv('heart.csv')
    real_x = data.iloc[:,[i for i in range(0, 13)]].values
    real_y = data.iloc[:,13].values
    training_x,test_x,training_y,test_y = train_test_split(real_x, real_y, test_size = 0.25, random_state = 0)
    working_data = pd.read_csv(fname)
    working_x = working_data.iloc[:,[i for i in range(1, 14)]].values
    s_c = StandardScaler()
    training_x = s_c.fit_transform(training_x)
    working_x = s_c.fit_transform(working_x)
    cls = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
    cls.fit(training_x, training_y)
    working_y = cls.predict(working_x)
    # print(working_y)
    return working_y

if __name__ == '__main__':
    result_lst = heart_prediction_patient("heart_patient_testing_data.csv")
