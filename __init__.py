from flask import Flask, render_template, jsonify,json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from datetime import datetime
from collections import Counter                                                                                                                                       
app = Flask(__name__)
@app.route('/commits/')
def commits():
    return render_template("commits.html")

@app.route('/get-commits-data/')
def get_commits_data():
    from urllib.request import urlopen
    import json
    from datetime import datetime
    
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    
    commits_by_minute = {}
    
    for commit in json_content:
        date_string = commit.get('commit', {}).get('author', {}).get('date')
        if date_string:
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute
            
            if minute in commits_by_minute:
                commits_by_minute[minute] += 1
            else:
                commits_by_minute[minute] = 1
    
    # Convertir notre dictionnaire en liste pour le JSON
    result = []
    for minute, count in commits_by_minute.items():
        result.append({'minute': minute, 'count': count})
    
    return jsonify(results=result)

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")                                                                                                                                     
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
if __name__ == "__main__":
  app.run(debug=True)
