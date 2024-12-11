import os
import pathlib
import sys
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/copyFile', methods=['POST'])
def copyFile():
    print("Copied Files!")
    print("basefile: ", request.form['basefile'])
    print("endfile: ",  request.form['endfile'])
    print("mapfile: ",  request.form['mapfile'])
    print("gemfile: ",  request.form['gemfile'])
    print("xlsxfile: ", request.form['xlsxfile'])

    baseFile = open("./data/" + request.form['basefile'], "r")
    endFile  = open("./data/" + request.form['endfile'],  "r")
    mapFile  = open("./data/" + request.form['mapfile'],  "r")
    gemFile  = open("./data/" + request.form['gemfile'],  "r")
    xlsxFile = open("./data/" + request.form['xlsxfile'], "r")
    return "Copied Files!"

@app.route('/preprocessMetabolome', methods=['POST'])
def preprocessMetabolome():
    command = 'python3 ./src/preprocess-metabolome.py'
    os.system(command)
    print("Preprocessed Metabolome!")
    return "Preprocessed Metabolome!"

@app.route('/preprocessHumanGem1', methods=['POST'])
def preprocessHumanGem1():
    command = 'python3 ./src/preprocess-human-gem-all.py'
    os.system(command)
    print("Preprocessed HumanGem1!")
    return "Preprocessed HumanGem1!"

@app.route('/preprocessHumanGem2', methods=['POST'])
def preprocessHumanGem2():
    command = 'python3 ./src/preprocess-human-gem-sets.py'
    os.system(command)
    print("Preprocessed HumanGem2")
    return "Preprocessed HumanGem2!"

@app.route('/featureGeneration1', methods=['POST'])
def featureGeneration1():
    command = 'python3 ./src/compute-change-feature.py -n 1'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 2'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 3'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 4'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 5'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 6'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 7'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 8'
    os.system(command)
    command = 'python3 ./src/compute-change-feature.py -n 9'
    os.system(command)
    print("Generated Feature1!")
    return "Generated Feature1!"

@app.route('/featureGeneration2', methods=['POST'])
def featureGeneration2():
    command = 'python3 ./src/compute-ratio-feature.py -n 1'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 2'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 3'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 4'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 5'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 6'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 7'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 8'
    os.system(command)
    command = 'python3 ./src/compute-ratio-feature.py -n 9'
    os.system(command)
    print("Generated Feature2!")
    return "Generated Feature2!"

@app.route('/featureGeneration3', methods=['POST'])
def featureGeneration3():
    command = 'python3 ./src/compute-prob-feature.py -n 1 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 2 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 3 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 4 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 5 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 6 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 7 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 8 -a 0'
    os.system(command)
    command = 'python3 ./src/compute-prob-feature.py -n 9 -a 0'
    os.system(command)
    print("Generated Feature3!")
    return "Generated Feature3!"

@app.route('/runClassification', methods=['POST'])
def runClassifcation():
    command = 'python3 ./src/run_classification.py'
    os.system(command)
    print("Run Classification!")
    return "Run Classification!"

@app.route('/generateSummary', methods=['POST'])
def generateSummary():
    treatments = ""

    if(request.form.get('diet.0')):
        treatments = treatments + " Almond"

    if(request.form.get('diet.1')):
        treatments = treatments + " Avocado"

    if(request.form.get('diet.2')):
        treatments = treatments + " Barley"

    if(request.form.get('diet.3')):
        treatments = treatments + " Broccoli"

    if(request.form.get('diet.4')):
        treatments = treatments + " Oats"

    if(request.form.get('diet.5')):
        treatments = treatments + " Walnut"
   
    print(treatments)

    command = 'python3 ./src/summarize_performance.py -t '
    os.system(command + '\'' + treatments + '\'')
    print("Generated Summary!")
    return "Generated Summary!"

if __name__ == '__main__':
    app.run(debug=True)
