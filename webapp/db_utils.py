import os, sys, random, json
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from main import db

def get_random_date_time():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - \
    timedelta(days=random.randint(1, 6), hours=random.randint(0, 12), seconds=random.randint(0, 60*60*7))

class Report(db.Model):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    entry_moment = Column(DateTime, default=func.now())
    disease_type = Column(String(250))
    gender = Column(String(15))
    age = Column(Integer)
    home_lat = Column(Float)
    home_lng = Column(Float)
    hospital_lat = Column(Float)
    hospital_lng = Column(Float)
    symptom_moment = Column(DateTime, default=func.now())

    def toDict(self):
        data = {}
        data['id'] = self.id
        data['entry_moment'] = self.entry_moment.isoformat()
        data['disease_type'] = self.disease_type
        data['gender'] = self.gender
        data['age'] = self.age
        data['hospital_lat'] = self.hospital_lat
        data['hospital_lng'] = self.hospital_lng
        data['symptom_moment'] = self.symptom_moment.isoformat()
        return data

    def toJson(self):
        return json.dumps(self.toDict())

    def to_string(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(self.id, self.entry_moment, self.disease_type, self.gender, self.age, self.hospital_lat, self.hospital_lng, self.symptom_moment)
        # return str(self.id) + "," + str(self.entry_moment) + "," + self.disease_type + "," + self.gender + "," + str(self.age) + "," + str(self.hospital_lat) + "," + str(self.hospital_lng) + "," + str(self.symptom_moment)

def add_report(disease_type, gender, age, hospital_lng, hospital_lat):
    report = Report(disease_type = disease_type, gender = gender, age = int(age), hospital_lat = float(hospital_lat), hospital_lng = float(hospital_lng), symptom_moment = get_random_date_time())
    db.session.add(report)
    db.session.commit()

def get_all_reports():
    reports = Report.query.all()
    return reports

def get_all_reports_from_loc(latitude, longitude):
    reports = Report.query.filter_by(hospital_lat=float(latitude), hospital_lng=float(longitude)).all()
    #return "\n".join([report.toJson() for report in reports])
    return reports

def get_top_reports(latitude=None, longitude=None):
    reports = db.session.query(Report.disease_type, db.func.count(Report.id).label('total')).\
        group_by(Report.disease_type).\
        order_by('total DESC').limit(10).all() \
        if not longitude else \
        db.session.query(Report.disease_type, db.func.count(Report.id).label('total')).\
            filter(Report.hospital_lat == float(latitude), Report.hospital_lng == float(longitude)).\
            group_by(Report.disease_type).\
            order_by('total DESC').limit(10).all()
    return reports

# this creates all the tables
db.create_all()
