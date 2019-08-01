#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 22:53:40 2019

@author: chuck
"""

import pandas as pd
from sklearn.preprocessing import Imputer
import matplotlib.pyplot as plt
import pickle
import requests
import json
import statsmodels.api as sm
from datetime import datetime
from pyramid.arima import auto_arima

#veriler = pd.read_excel("pizza-sales-data.xlsx", index_col=0)
veriler = pd.read_excel("pizza-sales-data.xlsx")
veriler.head()
veriler['DATE'] = pd.to_datetime(veriler['DATE'], format='%Y%d%m')
veriler['DATE'] = veriler['DATE'].dt.strftime('%Y/%d/%m')
veriler.index = veriler['DATE']
del veriler['DATE']

#del veriler['CATEGORY']
#veriler.index = pd.to_datetime(veriler.index, format='%Y%d%m')
#veriler.index = pd.to_datetime(veriler.index, format='%Y%d%m')
#veriler['DOB1'] = veriler['DOB1'].dt.strftime('%Y/%d/%m')

Neo =  veriler["CATEGORY"]=="Neapolitan Pizza"
NeopolitanPizza = veriler[Neo]
del NeopolitanPizza['CATEGORY']

imputer= Imputer
imputer= Imputer(missing_values='NaN', strategy = 'mean', axis=0 ) 
NeopolitanPizza[["SALES"]] = imputer.fit_transform(NeopolitanPizza[["SALES"]])

Sicilian =  veriler["CATEGORY"]=="Sicilian Pizza"
SicilianPizza = veriler[Sicilian]
del SicilianPizza['CATEGORY']

imputer= Imputer
imputer= Imputer(missing_values='NaN', strategy = 'mean', axis=0 ) 
SicilianPizza[["SALES"]] = imputer.fit_transform(SicilianPizza[["SALES"]])

Tomato =  veriler["CATEGORY"]=="Tomato Pie Pizza"
TomatoPiePizza = veriler[Tomato]
del TomatoPiePizza['CATEGORY']

imputer= Imputer
imputer= Imputer(missing_values='NaN', strategy = 'mean', axis=0 ) 
TomatoPiePizza[["SALES"]] = imputer.fit_transform(TomatoPiePizza[["SALES"]])

Chi =  veriler["CATEGORY"]!="Tomato Pie Pizza" 
ChicagoPizza = veriler[Chi]
Chi =  ChicagoPizza["CATEGORY"]!="Sicilian Pizza" 
ChicagoPizza = ChicagoPizza[Chi]
Chi =  ChicagoPizza["CATEGORY"]!="Neapolitan Pizza" 
ChicagoPizza = ChicagoPizza[Chi]
del ChicagoPizza['CATEGORY']

imputer= Imputer
imputer= Imputer(missing_values='NaN', strategy = 'mean', axis=0 ) 
ChicagoPizza[["SALES"]] = imputer.fit_transform(ChicagoPizza[["SALES"]])

stepwise_model = auto_arima(NeopolitanPizza, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=4,
                           start_P=0, seasonal=True,
                           d=0, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
print(stepwise_model.aic())

train_Neo = NeopolitanPizza.loc['2016-01-01':'2018-01-01']
test_Neo = NeopolitanPizza.loc['2018-01-01':]

send_periods = 10;
date_rng = pd.date_range(start='2018-01-01', periods= send_periods, freq='M')

date_rng = pd.DataFrame(data = date_rng, index = range(send_periods), columns=['DATES'] )
date_rng.index = date_rng['DATES']
del date_rng['DATES']
test_Neo = pd.concat([test_Neo,date_rng],axis=1)

stepwise_model.fit(train_Neo)
future_forecast = stepwise_model.predict(n_periods=17)
print(future_forecast)
future_forecast = pd.DataFrame(future_forecast, index=test_Neo.index, columns=['Prediction'])
pd.concat([test_Neo, future_forecast], axis=1).plot()
plt.show()

pd.concat([NeopolitanPizza,future_forecast],axis=1).plot()

model=sm.tsa.statespace.SARIMAX(endog=NeopolitanPizza['SALES'],order=(0,1,1),seasonal_order=(1,1,1,4),trend='c',enforce_invertibility=False)
results=model.fit()
print(results.summary())

save_neopolitan_pred = pd.concat([test_Neo, future_forecast], axis=1)
hist_df = pd.DataFrame(save_neopolitan_pred) 

hist_json_file = 'history_sicilian_prediction.json' 
with open(hist_json_file, mode='w') as f:
    hist_df.to_json(f)

hist_csv_file = 'history_sicilian_prediction.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

#predict_dy = results.get_prediction(start=pd.to_datetime('2019-01-01'), end=pd.to_datetime('2020-01-01'), freq='M', full_results=True, dynamic=True)
#predict_dy_ci = predict_dy.conf_int()
#predict_dy = results.predict(start=pd.to_datetime('2018-01-01'), end=pd.to_datetime('2019-01-01'), freq='M', dynamic=True)
#print(predict_dy)

stepwise_model2 = auto_arima(SicilianPizza, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=5,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
print(stepwise_model2.aic())

train_Sic = SicilianPizza.loc['2016-01-01':'2018-01-01']
test_Sic = SicilianPizza.loc['2018-01-01':]

send_periods = 10;
date_rng_Sic = pd.date_range(start='2018-01-01', periods= send_periods, freq='M')

date_rng_Sic = pd.DataFrame(data = date_rng_Sic, index = range(send_periods), columns=['DATES'] )
date_rng_Sic.index = date_rng_Sic['DATES']
del date_rng_Sic['DATES']
test_Sic = pd.concat([test_Sic,date_rng_Sic],axis=1)

stepwise_model2.fit(train_Sic)

future_forecast2 = stepwise_model2.predict(n_periods=17)
print(future_forecast2)
future_forecast2 = pd.DataFrame(future_forecast2, index=test_Sic.index, columns=['Prediction'])
pd.concat([test_Sic, future_forecast2], axis=1).plot()
plt.show()

pd.concat([SicilianPizza,future_forecast2],axis=1).plot()

model=sm.tsa.statespace.SARIMAX(endog=SicilianPizza['SALES'],order=(0,0,0),seasonal_order=(2,1,1,5),trend='c',enforce_invertibility=False)
results=model.fit()
print(results.summary())

save_sicilian_pred = pd.concat([test_Sic, future_forecast2], axis=1)
hist_df = pd.DataFrame(save_sicilian_pred) 

hist_json_file = 'history_sicilian_prediction.json' 
with open(hist_json_file, mode='w') as f:
    hist_df.to_json(f)

hist_csv_file = 'history_sicilian_prediction.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

stepwise_model3 = auto_arima(ChicagoPizza, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=8,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
print(stepwise_model3.aic())

train_Chic = ChicagoPizza.loc['2016-01-01':'2018-01-01']
test_Chic = ChicagoPizza.loc['2018-01-01':]

send_periods = 10;
date_rng_Chic = pd.date_range(start='2018-01-01', periods= send_periods, freq='M')

date_rng_Chic = pd.DataFrame(data = date_rng_Chic, index = range(send_periods), columns=['DATES'] )
date_rng_Chic.index = date_rng_Chic['DATES']
del date_rng_Chic['DATES']
test_Chic = pd.concat([test_Chic,date_rng_Chic],axis=1)

stepwise_model3.fit(train_Chic)

future_forecast3 = stepwise_model3.predict(n_periods=17)
print(future_forecast3)
future_forecast3 = pd.DataFrame(future_forecast3, index=test_Chic.index, columns=['Prediction'])
pd.concat([test_Chic, future_forecast3], axis=1).plot()
plt.show()

pd.concat([ChicagoPizza,future_forecast3],axis=1).plot()

model=sm.tsa.statespace.SARIMAX(endog=ChicagoPizza['SALES'],order=(2,1,1),seasonal_order=(0,1,0,7),trend='c',enforce_invertibility=False)
results=model.fit()
print(results.summary())

save_chicago_pred = pd.concat([test_Chic, future_forecast3], axis=1)
hist_df = pd.DataFrame(save_chicago_pred)      

hist_json_file = 'history_chicago_prediction.json' 
with open(hist_json_file, mode='w') as f:
    hist_df.to_json(f)

hist_csv_file = 'history_chicago_prediction.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

stepwise_model4 = auto_arima(TomatoPiePizza, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=6,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
print(stepwise_model4.aic())

train_Tom = TomatoPiePizza.loc['2016-01-01':'2018-01-01']
test_Tom = TomatoPiePizza.loc['2018-01-01':]

send_periods = 10;
date_rng_Tom = pd.date_range(start='2018-01-01', periods= send_periods, freq='M')

date_rng_Tom = pd.DataFrame(data = date_rng_Tom, index = range(send_periods), columns=['DATES'] )
date_rng_Tom.index = date_rng_Tom['DATES']
del date_rng_Tom['DATES']
test_Tom = pd.concat([test_Tom,date_rng_Tom],axis=1)

stepwise_model4.fit(train_Tom)

future_forecast4 = stepwise_model4.predict(n_periods=17)
print(future_forecast4)
future_forecast4 = pd.DataFrame(future_forecast4, index=test_Tom.index, columns=['Prediction'])
pd.concat([test_Tom, future_forecast4], axis=1).plot()
plt.show()

pd.concat([TomatoPiePizza,future_forecast4],axis=1).plot()

model=sm.tsa.statespace.SARIMAX(endog=TomatoPiePizza['SALES'],order=(0,1,1),seasonal_order=(0,1,0,6),trend='c',enforce_invertibility=False)
results=model.fit()
print(results.summary())

save_tomato_pred = pd.concat([test_Tom, future_forecast4], axis=1)
hist_df = pd.DataFrame(save_tomato_pred) 

hist_json_file = 'history_tomatopie_prediction.json' 
with open(hist_json_file, mode='w') as f:
    hist_df.to_json(f)

hist_csv_file = 'history_tomatopie_prediction.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

