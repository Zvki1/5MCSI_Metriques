from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from datetime import datetime
from collections import Counter                                                                                                                                       
app = Flask(__name__)
@app.route("/commits/")
def commits():
    return render_template("commits.html") 
@app.route('/api/commits/')
def commits_data():
    url = 'https://api.github.com/repos/Zvki1/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits = response.json()

    # Compter les minutes
    minutes_counter = Counter()

    for commit in commits:
        try:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_obj.minute
            minutes_counter[minute] += 1
        except KeyError:
            continue  # En cas de commit mal formé

    # Formatage pour le frontend
    result = [{'minute': str(minute).zfill(2), 'count': count} for minute, count in sorted(minutes_counter.items())]
    return jsonify(result)
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
