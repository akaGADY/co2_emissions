# -*- coding: utf-8 -*-
"""co.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HdcgIvYyoQe5zcML_YERkXTaoa9fOAqt
"""
! pip install scipy
import streamlit as st
import pandas as pd
import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Function to load or train the Random Forest model
def load_or_train_model():
    df = pd.read_csv('co2_emissions (1).csv')
    #dropping all duplicates values
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df_natural = df[df['fuel_type']=='Natural Gas']
    natural = df_natural.index
    #removing natural gas from the dataset
    for i in natural:
      df.drop(i,axis=0,inplace=True)
    df.reset_index(drop=True,inplace=True)
    df_correlation = df[['engine_size','cylinders','fuel_consumption_city','fuel_consumption_hwy','fuel_consumption_comb(l/100km)','fuel_consumption_comb(mpg)','co2_emissions']]
    z = np.abs(stats.zscore(df_correlation))
    df_new = df_correlation[(z < 1.9).all(axis=1)]
    df_new.reset_index(drop=True,inplace = True)
    sample_df = df_new.sample(n=200,random_state=35)
    indexs = sample_df.index
    # we have to drop the sample dataframes
    for i in indexs:
      df_new.drop(i, axis = 0,inplace = True)
    sample_df_x = sample_df.drop(['co2_emissions'],axis=1)
    sample_df_y = sample_df['co2_emissions']
    new = sample_df_x.astype(np.float32)
    sample_df_x = (new - np.min(new)) / (np.max(new) - np.min(new))
    sample_df_x['engine_size'] = sample_df_x['engine_size'].map(lambda x:round(x,2))
    sample_df_x['cylinders']=sample_df_x["cylinders"].map(lambda x:round(x,2))
    sample_df_x['fuel_consumption_city']=sample_df_x["fuel_consumption_city"].map(lambda x:round(x,2))
    sample_df_x['fuel_consumption_hwy']=sample_df_x["fuel_consumption_hwy"].map(lambda x:round(x,2))
    sample_df_x['fuel_consumption_comb(l/100km)']=sample_df_x['fuel_consumption_comb(l/100km)'].map(lambda x:round(x,2))
    sample_df_x['fuel_consumption_comb(mpg)']=sample_df_x["fuel_consumption_comb(mpg)"].map(lambda x:round(x,2))
    ## NORMALIZATION
    X = df_new.drop(['co2_emissions'], axis= 1).astype(np.float32)
    y = df_new['co2_emissions'].astype(np.float32)
    X['engine_size']=X['engine_size'].map(lambda x:round(x,2))
    X["cylinders"]=X["cylinders"].map(lambda x:round(x,2))
    X["fuel_consumption_city"]=X["fuel_consumption_city"].map(lambda x:round(x,2))
    X["fuel_consumption_hwy"]=X["fuel_consumption_hwy"].map(lambda x:round(x,2))
    X['fuel_consumption_comb(l/100km)']=X['fuel_consumption_comb(l/100km)'].map(lambda x:round(x,2))
    X["fuel_consumption_comb(mpg)"]=X["fuel_consumption_comb(mpg)"].map(lambda x:round(x,2))



    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=42, test_size=0.2)


    # Initialize and train the Random Forest model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    return model

def main():
    st.title('Random Forest Regression Model Deployment')

    st.write('Enter the following details to predict CO2 Emissions:')

    engine_size = st.number_input('Engine Size', min_value=0.0, step=0.1)
    cylinders = st.number_input('Cylinders', min_value=0, step=1)
    fuel_consumption_city = st.number_input('Fuel Consumption City (l/100km)', min_value=0.0, step=0.1)
    fuel_consumption_highway = st.number_input('Fuel Consumption Highway (l/100km)', min_value=0.0, step=0.1)
    fuel_consumption_combined = st.number_input('Fuel Consumption Combined (l/100km)', min_value=0.0, step=0.1)
    fuel_consumption_combined_mpg = st.number_input('Fuel Consumption Combined (mpg)', min_value=0.0, step=0.1)

    if st.button('Predict'):
        # Load or train the Random Forest model
        model = load_or_train_model()

        # Predict CO2 emissions using the trained model
        input_data = np.array([[engine_size, cylinders, fuel_consumption_city, fuel_consumption_highway, fuel_consumption_combined, fuel_consumption_combined_mpg]])
        predicted_co2 = model.predict(input_data)

        st.write(f'Predicted CO2 Emissions: {predicted_co2[0]} g/km')

if __name__ == '__main__':
    main()
