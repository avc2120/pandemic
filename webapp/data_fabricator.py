import os
import random

from main import db
import db_utils

diseases = [line.replace('\n','').replace(',','-') for line in open('data/all_infectious_diseases.txt', 'r').readlines()]
hospital_labels = ['name', 'latitude', 'longitude']
hospitals = [dict(zip(hospital_labels,line.replace('\n','').split(','))) for line in open('data/hospital_locations.txt', 'r').readlines()]
genders = ['male', 'female', 'non-binary']

def populate_db():
    for i in range(2000):
        disease_type = random.choice(diseases)
        gender = random.choice(genders)
        age = random.randint(0, 90)
        hospital = random.choice(hospitals)
        hospital_lat = hospital['latitude']
        hospital_lng = hospital['longitude']
        db_utils.add_report(disease_type, gender, age, hospital_lng, hospital_lat)

    print("Data has been successfully fabricated!")
