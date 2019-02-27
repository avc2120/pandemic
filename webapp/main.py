from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import docusign_client, here_client
import json

app = Flask(__name__)
app.run(debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import db_utils, data_fabricator

# populates the db on startup
data_fabricator.populate_db()

@app.route('/', methods=["GET"])
def hello_world():
    longitude=-122.419418
    latitude=37.774929
    return render_template('index.html', longitude=longitude, latitude=latitude)

#http://localhost:5000/setLocation?longitude=-122.08979&latitude=37.41291
@app.route('/setLocation', methods=["GET","POST"])
def set_location():
    location = request.args.get('location')
    response = here_client.get_geocode_from_search(location)
    print(type(response))
    if response:
        response = json.loads(response)
        print(type(response))
        myLatLng = response.get("Response").get("View")[0].get("Result")[0].get("Location").get("NavigationPosition")[0]
    print(myLatLng)
    longitude = myLatLng["Longitude"]
    latitude = myLatLng["Latitude"]
    print(longitude, latitude)
    if longitude == None or latitude == None:
        longitude=37.774929
        latitude=-122.419418
        print("IN HERE")
    return render_template('index.html', longitude=longitude, latitude=latitude)

@app.route('/predict', methods=['GET'])
def identify_image():
    url = request.args.get('url')
    if not url:
        return "Missing url query parameter"
    return ' | '.join(clarifai_client.predict(url))

@app.route('/geocode', methods=['GET'])
def get_geocode():
    searchtext = request.args.get('searchtext')
    if not searchtext:
        return "Missing searchtext query parameter"
    return here_client.get_geocode_from_search(searchtext)

@app.route('/sign')
def sign_doc_init():
    return redirect(docusign_client.embedded_signing_ceremony(), code=302)

@app.route('/template_1')
def template_1():
    tocdc = request.args.get('tocdc')
    if tocdc == 'true':
        return redirect(docusign_client.get_signing_redirect(3), code=302)
    return redirect(docusign_client.get_signing_redirect(0), code=302)

@app.route('/template_2')
def template_2():
    return redirect(docusign_client.get_signing_redirect(1), code=302)

@app.route('/signing_complete')
def signing_complete():
    return render_template('warning.html')

@app.route('/report_complete')
def report_complete():
    return render_template('success.html')

# {Content-Type: application/json}
@app.route('/add_report', methods=['POST'])
def add_report():
    data = request.get_json()
    disease_type = data.get('disease_type')
    gender = data.get('gender')
    age = data.get('age')
    hospital_lng = data.get('hospital_lng')
    hospital_lat = data.get('hospital_lat')
    db_utils.add_report(disease_type, gender, age, hospital_lng, hospital_lat)
    return db_utils.get_all_reports()

@app.route('/get_top_reports', methods=['GET'])
def get_top_reports():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    labels = ['disease', 'count']
    return jsonify([dict(zip(labels, group)) for group in db_utils.get_top_reports(latitude, longitude)])

# http://localhost:5000/get_reports?latitude=37.763078&longitude=-122.4599797
@app.route('/get_reports')
def get_reports():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return jsonify([report.toDict() for report in db_utils.get_all_reports_from_loc(latitude, longitude)])

# FOR TESTING
# ?disease_type=ebola&gender=male&age=21&hospital_lng=-122.419418&hospital_lat=37.774929
@app.route('/add_report_param')
def add_report_param():
    disease_type = request.args.get('disease_type')
    gender = request.args.get('gender')
    age = request.args.get('age')
    hospital_lng = request.args.get('hospital_lng')
    hospital_lat = request.args.get('hospital_lat')
    db_utils.add_report(disease_type, gender, age, hospital_lng, hospital_lat)
    return jsonify([report.toDict() for report in db_utils.get_all_reports()])
