# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect = True)

# Save references to each table
station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
#1
@app.route("/")
def welcome():
    return(
        f"Welcome to the Climate App<br/>"
        f"Routes:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/start (YYYY-MM-DD)<br/>"
         )

#2
@app.route("/api.v1.0/precipitation")

def precipitation():
  session = Session(engine)

yearly_rainfall = dt.date(2017, 8, 23)-dt.timedelta(days = 365)
previous_date = dt.date(yearly_rainfall.year, yearly_rainfall.month, yearly_rainfall.day)

values= session.query(measurement.date, measurement.prcp).filter(measurement.date >= previous_date).order_by(measurement.date.desc()).all()
p_dict = dict(values)
print(f"Precipitation Values - {p_dict}")
print("Precipitation Station")
#return jsonify(p_dict)

#3
@app.route("/api/v1.stations")
def stations():
  session = Session(engine)
  select = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
  queryresult = session.query(*sel).all()
  session.close
  
  stations = []
  for station, name, lat, lon, el, in queryresult:
      station_dict = {}
      station_dict["Station"] = station
      station_dict["Name"] = name
      station_dict["Elevation"] = el
      station_dict["Lat"] = lat
      station_dict["Long"] = lon
      stations.append(station_dict)
  return jsonify(stations)

  #4
  @app.route("/api/v1.0/tobs")
  def tobs():
      session.Session(engine)

      result = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281')\
        .filter(measurement.date >= '2016-08-23').all()

      tob_obs = []
      for date, tobs in queryresult:
          tobs_dict = {}
          tobs_dict["Date"] = date
          tobs_dict["Tobs"] = tobs
          tob_obs.append(tobs_dict)

      return jsonify(tob_obs)

      #5

  @app.route("/api/v1.0/<start>")

  def get_temps_start(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(Measurement.tobs)).\
              filter(measurement.date >= start).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)