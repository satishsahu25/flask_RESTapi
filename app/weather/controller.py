# https://api.openweathermap.org/data/2.5/weather?lat=70&lon=-94.05&appid=XXXXXXXXXXXXXX
from flask import request
import requests
from app import app


baseurl="https://api.openweathermap.org/data/2.5/weather?"
@app.route("/getweather",methods=["GET"])
def getweatherdata():
    data=request.get_json()
    lat=data['lat']
    long=data['long']
    params=dict(lat=lat,lon=long,appid="XXXXXXXXXXXXXX")
    data=requests.get(url=baseurl,params=params)
    print(data.content)
    return data.content


