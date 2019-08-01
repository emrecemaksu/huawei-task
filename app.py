from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.preprocessing import Imputer
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime
from pyramid.arima import auto_arima
import pickle
import requests
import json
import os
from flask_jsonpify import jsonpify

TASKS = [
    {
        'user': 'root',    
        'name': 'Task 1',
        'step': 10,
        'status': 'Success',
        'Neopolitan_Pred': [[94.58663138835229], [95.23027905717272], [67.69729978162803], [63.26480755394208], [91.22818088524912], [97.34316161314263], [57.841641270875584], [57.17069052130237], [92.51579197442919], [95.43129021345281], [62.92863781558865], [60.05804285491739], [91.08651623799906], [95.87298231722932], [59.27758776891316], [57.69328319838395], [91.24599990059075]],
        'Neopolitan': [[95.0], [69.0], [82.0], [68.0], [58.0], [96.0], [91.0], [87.0], [81.0], [59.0], [92.0], [70.0], [60.0], [76.0], [87.0], [70.0], [99.0], [93.0], [80.0], [71.0], [90.0], [100.0], [52.0], [54.0], [70.0], [68.0], [64.0], [51.0], [75.86666666666666], [90.0], [53.0]],
        'Sicilian': [[50.0], [94.0], [70.0], [91.0], [76.0], [95.0], [89.0], [95.0], [87.0], [51.0], [61.0], [75.0], [86.0], [73.0], [62.0], [80.0], [84.0], [60.0], [75.0], [81.0], [70.0], [81.0], [85.0], [78.0], [55.0], [80.0], [60.0], [81.0], [84.0], [85.0], [62.0]],
        'Sicilian_Pred': [[54.989261993576115], [68.16620615083377], [80.0170028486223], [71.71981205723392], [75.84246618979661], [63.565254224114376], [67.04066460176877], [78.56654193901096], [75.22964269842848], [74.89830957782537], [58.323531563249055], [65.71583466188025], [77.38940545063411], [72.07565745307167], [73.55181512541753], [58.72164991152982], [64.55652835780879]],
        'Chicago': [[95.0], [50.0], [92.0], [75.0], [84.0], [86.0], [65.0], [87.0], [77.06666666666666], [72.0], [94.0], [53.0], [81.0], [62.0], [96.0], [72.0], [86.0], [95.0], [60.0], [100.0], [85.0], [89.0], [62.0], [84.0], [68.0], [51.0], [81.0], [92.0], [79.0], [52.0], [64.0]],
        'Chicago_Pred': [[78.3547927793002], [74.60998992898205], [85.06213847382912], [58.43456938479636], [77.4092825318184], [61.78226991552428], [83.23387000426584], [67.06418137076156], [76.40076505435172], [82.00416723894827], [54.79207300326423], [81.08683419184877], [71.66832325200512], [70.97087450228885], [52.32133452398412], [66.0749823127231], [62.36779773020313]],
        'TomatoPie': [[80.0], [77.0], [99.0], [62.0], [83.0], [60.0], [77.0], [53.0], [87.0], [65.0], [99.0], [72.0], [85.0], [69.0], [76.0], [75.0], [81.0], [66.0], [75.23333333333333], [78.0], [67.0], [89.0], [80.0], [50.0], [79.0], [76.0], [54.0], [79.0], [88.0], [80.0], [71.0]],
        'TomatoPie_Pred': [[73.66664710766439], [76.39566027077781], [65.35800676722455], [87.32035326367131], [78.28269976011806], [48.245046256564805], [71.87403986067595], [74.56539952023611], [63.49009251312959], [85.4147855060231], [76.33947849891659], [46.264171491810096], [69.85551159236799], [72.5092177483749], [61.39625723771513], [83.28329672705539], [74.17033621639564]]
    },
    {
        'user': 'root',
        'name': 'Task 2',
        'step': 5,
        'status': 'Success',
        'Neopolitan_Pred': [[94.58663138835229], [95.23027905717272], [67.69729978162803], [63.26480755394208], [91.22818088524912], [97.34316161314263], [57.841641270875584], [57.17069052130237], [92.51579197442919], [95.43129021345281], [62.92863781558865], [60.05804285491739]],
        'Neopolitan': [[95.0], [69.0], [82.0], [68.0], [58.0], [96.0], [91.0], [87.0], [81.0], [59.0], [92.0], [70.0], [60.0], [76.0], [87.0], [70.0], [99.0], [93.0], [80.0], [71.0], [90.0], [100.0], [52.0], [54.0], [70.0], [68.0], [64.0], [51.0], [75.86666666666666], [90.0], [53.0]],
        'Sicilian': [[50.0], [94.0], [70.0], [91.0], [76.0], [95.0], [89.0], [95.0], [87.0], [51.0], [61.0], [75.0], [86.0], [73.0], [62.0], [80.0], [84.0], [60.0], [75.0], [81.0], [70.0], [81.0], [85.0], [78.0], [55.0], [80.0], [60.0], [81.0], [84.0], [85.0], [62.0]],
        'Sicilian_Pred': [[54.989261993576115], [68.16620615083377], [80.0170028486223], [71.71981205723392], [75.84246618979661], [63.565254224114376], [67.04066460176877], [78.56654193901096], [75.22964269842848], [74.89830957782537], [58.323531563249055], [65.71583466188025]],
        'Chicago': [[95.0], [50.0], [92.0], [75.0], [84.0], [86.0], [65.0], [87.0], [77.06666666666666], [72.0], [94.0], [53.0], [81.0], [62.0], [96.0], [72.0], [86.0], [95.0], [60.0], [100.0], [85.0], [89.0], [62.0], [84.0], [68.0], [51.0], [81.0], [92.0], [79.0], [52.0], [64.0]],
        'Chicago_Pred': [[78.3547927793002], [74.60998992898205], [85.06213847382912], [58.43456938479636], [77.4092825318184], [61.78226991552428], [83.23387000426584], [67.06418137076156], [76.40076505435172], [82.00416723894827], [54.79207300326423], [81.08683419184877]],
        'TomatoPie': [[80.0], [77.0], [99.0], [62.0], [83.0], [60.0], [77.0], [53.0], [87.0], [65.0], [99.0], [72.0], [85.0], [69.0], [76.0], [75.0], [81.0], [66.0], [75.23333333333333], [78.0], [67.0], [89.0], [80.0], [50.0], [79.0], [76.0], [54.0], [79.0], [88.0], [80.0], [71.0]],
        'TomatoPie_Pred': [[73.66664710766439], [76.39566027077781], [65.35800676722455], [87.32035326367131], [78.28269976011806], [48.245046256564805], [71.87403986067595], [74.56539952023611], [63.49009251312959], [85.4147855060231], [76.33947849891659], [46.264171491810096]]
    },
    {
        'user': 'root',
        'name': 'Task 3',
        'step': 2,
        'status': 'Success',
        'Neopolitan_Pred': [[94.58663138835229], [95.23027905717272], [67.69729978162803], [63.26480755394208], [91.22818088524912], [97.34316161314263], [57.841641270875584], [57.17069052130237], [92.51579197442919]],
        'Neopolitan': [[95.0], [69.0], [82.0], [68.0], [58.0], [96.0], [91.0], [87.0], [81.0], [59.0], [92.0], [70.0], [60.0], [76.0], [87.0], [70.0], [99.0], [93.0], [80.0], [71.0], [90.0], [100.0], [52.0], [54.0], [70.0], [68.0], [64.0], [51.0], [75.86666666666666], [90.0], [53.0]],
        'Sicilian': [[50.0], [94.0], [70.0], [91.0], [76.0], [95.0], [89.0], [95.0], [87.0], [51.0], [61.0], [75.0], [86.0], [73.0], [62.0], [80.0], [84.0], [60.0], [75.0], [81.0], [70.0], [81.0], [85.0], [78.0], [55.0], [80.0], [60.0], [81.0], [84.0], [85.0], [62.0]],
        'Sicilian_Pred': [[54.989261993576115], [68.16620615083377], [80.0170028486223], [71.71981205723392], [75.84246618979661], [63.565254224114376], [67.04066460176877], [78.56654193901096], [75.22964269842848]],
        'Chicago': [[95.0], [50.0], [92.0], [75.0], [84.0], [86.0], [65.0], [87.0], [77.06666666666666], [72.0], [94.0], [53.0], [81.0], [62.0], [96.0], [72.0], [86.0], [95.0], [60.0], [100.0], [85.0], [89.0], [62.0], [84.0], [68.0], [51.0], [81.0], [92.0], [79.0], [52.0], [64.0]],
        'Chicago_Pred': [[78.3547927793002], [74.60998992898205], [85.06213847382912], [58.43456938479636], [77.4092825318184], [61.78226991552428], [83.23387000426584], [67.06418137076156], [76.40076505435172]],
        'TomatoPie': [[80.0], [77.0], [99.0], [62.0], [83.0], [60.0], [77.0], [53.0], [87.0], [65.0], [99.0], [72.0], [85.0], [69.0], [76.0], [75.0], [81.0], [66.0], [75.23333333333333], [78.0], [67.0], [89.0], [80.0], [50.0], [79.0], [76.0], [54.0], [79.0], [88.0], [80.0], [71.0]],
        'TomatoPie_Pred': [[73.66664710766439], [76.39566027077781], [65.35800676722455], [87.32035326367131], [78.28269976011806], [48.245046256564805], [71.87403986067595], [74.56539952023611], [63.49009251312959]]
    }
]

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
"""
model_Chicago = pickle.load(open('model_Chicago_Save.pkl','rb'))

model_Tomato = pickle.load(open('model_TomatoPie_Save.pkl','rb'))
model_Neopolitan = pickle.load(open('model_Neo_Save.pkl','rb'))

model_Sicilian = pickle.load(open('model_Sicilian_Save.pkl','rb'))
"""
@app.route('/api',methods=['GET', 'POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    prediction = model_Sicilian.predict(n_periods=17)
    return jsonify(prediction)

@app.route('/json', methods=['GET', 'POST'])
def all_tasks():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "client/upload/pizza-sales-data.xlsx"
    abs_file_path = os.path.join(script_dir, rel_path)
    veriler = pd.read_excel(abs_file_path)
    veriler.head()
    veriler['DATE'] = pd.to_datetime(veriler['DATE'], format='%Y%d%m')
    veriler['DATE'] = veriler['DATE'].dt.strftime('%Y/%d/%m')
    veriler.index = veriler['DATE']
    del veriler['DATE']
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
    response_object = {'status': 'success'}
    
    stepwise_model = auto_arima(NeopolitanPizza, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=4,
                           start_P=0, seasonal=True,
                           d=0, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
    
    train_Neo = NeopolitanPizza.loc['2016-01-01':'2018-01-01']
    test_Neo = NeopolitanPizza.loc['2018-01-01':]
    
    send_periods = 2;
    date_rng = pd.date_range(start='2018-01-01', periods= send_periods, freq='M')
    
    date_rng = pd.DataFrame(data = date_rng, index = range(send_periods), columns=['DATES'] )
    date_rng.index = date_rng['DATES']
    del date_rng['DATES']
    test_Neo = pd.concat([test_Neo,date_rng],axis=1)
    
    stepwise_model.fit(train_Neo)
    
    future_forecast = stepwise_model.predict(n_periods=9)
    future_forecast = pd.DataFrame(future_forecast, index=test_Neo.index, columns=['Prediction'])    
  
    
    stepwise_model2 = auto_arima(SicilianPizza, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=5,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
    
    train_Sic = SicilianPizza.loc['2016-01-01':'2018-01-01']
    test_Sic = SicilianPizza.loc['2018-01-01':]
    
    send_periods = 5;
    date_rng_Sic = pd.date_range(start='2018-01-01', periods= send_periods, freq='M')
    
    date_rng_Sic = pd.DataFrame(data = date_rng_Sic, index = range(send_periods), columns=['DATES'] )
    date_rng_Sic.index = date_rng_Sic['DATES']
    del date_rng_Sic['DATES']
    test_Sic = pd.concat([test_Sic,date_rng_Sic],axis=1)
    
    stepwise_model2.fit(train_Sic)
        
    future_forecast2 = stepwise_model2.predict(n_periods=12)
    future_forecast2 = pd.DataFrame(future_forecast2, index=test_Sic.index, columns=['Prediction'])   
    
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
    future_forecast3 = pd.DataFrame(future_forecast3, index=test_Chic.index, columns=['Prediction'])
    
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
    future_forecast4 = pd.DataFrame(future_forecast4, index=test_Tom.index, columns=['Prediction'])
  
    if request.method == 'POST':
        post_data = request.get_json()
        TASKS.append({
            'user': post_data.get('user'),
            'name': post_data.get('name'),
            'step': post_data.get('step'),
            'status': post_data.get('status'),
            'frame': post_data.get('frame')
        })
        response_object['message'] = 'New Task Added!'
    else:
        response_object['tasks'] = TASKS
    df_list = future_forecast4.values.tolist()
    JSONP_data = jsonpify(df_list)
    #return JSONP_data
    return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug = True)
    

