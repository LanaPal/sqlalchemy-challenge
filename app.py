import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime, timedelta

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# #save references to the tables (measurement, station)
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask set up
app = Flask(__name__)

# #flask routes 
#root - main page
@app.route("/")
def root():
    """List all available API routes"""
    return (
        f"Available API routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"//api/v1.0/startend")

#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
#create session (link) from python to db
    session = Session(engine)
    # Perform a query to retrieve the data and precipitation scores for 12 months period starting from 2016-8-23
    # Convert the query results to a dictionary using date as the key and prcp as the value
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > dt.date(2016, 8, 23)).\
    order_by(Measurement.date.desc()).all()
    
    session.close()
    #convert results into list
    perc_data = list(np.ravel(results))
    return jsonify(perc_data)

#stations route
@app.route("/api/v1.0/stations")
def stations():
#create session (link) from python to db
    session = Session(engine)
    ## List the stations and the counts of weather observations in the descending order.
    results = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    
    session.close()
    #convert results into list
    station_data = list(np.ravel(results))
    return jsonify(station_data)

#route for tobs/observations query
@app.route("/api/v1.0/tobs")
def tobs():
#create session (link) from python to db
    session = Session(engine)
    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').all()
    
    session.close()
    #convert results into list
    tobs_data = list(np.ravel(results))
    return jsonify(tobs_data)

#route for the start date query
@app.route("/api/v1.0/start")
def start_date():
    #create session (link) from python to db
    session = Session(engine)
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    #start vacation date: 2017-7-20, end date: 2017-8-01
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= dt.date(2017, 7, 20)).all()
    
    session.close()
    #convert results into list
    start_data = list(np.ravel(results))
    return jsonify(start_data)

#route for the start end date range query
@app.route("/api/v1.0/startend")
def end_date():
    #create session (link) from python to db
    session = Session(engine)
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #start vacation date: 2017-7-20, end date: 2017-8-01
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= dt.date(2017, 7, 20)).\
    filter(Measurement.date <= dt.date(2017, 8, 1)).\
    order_by(Measurement.date.desc()).all()
    
    session.close()
    #convert results into list
    end_data = list(np.ravel(results))
    return jsonify(end_data)

if __name__ == "__main__":
    app.run(debug=True)
