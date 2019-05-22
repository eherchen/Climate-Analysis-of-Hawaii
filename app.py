import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def home():
    return('Hello World')

@app.route("/api/v1.0/precipitation")
def precipitation():
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_twelve_months = dt.datetime.strptime(latest_date, '%Y-%m-%d') - relativedelta(months=+12)
    prev_year_data = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                    filter(Measurement.date >= last_twelve_months).\
                    group_by(Measurement.date).all()

   
    all_precipitation = []
    for date, prcp in prev_year_data:
        precipitation_dict = {date:prcp}
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    activity_stations = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()

   
    all_stations = []
    for station, count in activity_stations:
        stations_dict = {station:count}
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_twelve_months = dt.datetime.strptime(latest_date, '%Y-%m-%d') - relativedelta(months=+12)
    annual_temp_data = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= last_twelve_months).\
                    group_by(Measurement.date).all()
    
    all_tobs = []
    for date, tobs in annual_temp_data:
        tobs_dict = {date:tobs}
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start=None,end=None):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all() 

    all_calc_temps = []
    for tobs in results:
        calc_temps_dict = {tobs}
        all_calc_temps.append(calc_temps_dict)
                
    # if not end:
    return jsonify(all_calc_temps)


# print(calc_temps('2012-02-28', '2012-03-05'))

if __name__ == "__main__":
    app.run(debug=True)

