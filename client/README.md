I chose to use the Vue.JS framework. Because Vue has a simple approach. Vue is great when it comes to integration with other libraries, like Bootstrap.
I chose to use Flask web application framework.
I chose to use JSON.
I chose to use ARIMA for Dataset. Because dataset shows sales in time series.
I chose to use Spyder IDE and Python3 for create model

I installed the Npm package manager for the VUE. (sudo npm install --save). (sudo npm install --package-name) for other packages.
I installed Flask (sudo pip3 install Flask)


I started Vue.JS (sudo npm run dev) http://localhost:8080/
I started Flask (sudo python3 app.py) http://127.0.0.1:5000/json

I created a ARIMA Model for dataset. And I import the model to the Flask.

!!! I saved models with Pickle. But each task has different files. So the model will also change. I din't use Pickle.

I want to apply dockerization the application and I want share Heroku. 
But I get "Docker requires Windows 10 Pro or Enterprise version 14393 to run" message. Because I use Windows 10 Home.
So I don't apply what I want
these are the codes I want to apply to make the applications I planned ;

build the image and run the container in detached mode =>

> docker build -t web:latest
> docker run -d --name huawei-task -e "PORT=8765" -p 8007:8765 web:latest
> docker exec huawei-task cat ../nginx/conf.d/default.conf
> docker stop huawei-task

If docker will work :

> heroku create
> heroku container:login
> registry.heroku.com/huawei-task/web
> docker build -t registry.heroku.com/huawei-task/web
> docker push registry.heroku.com/huawei-task/web
> heroku container:release --app huawei-task web

