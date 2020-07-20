import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask set up
app = Flask(__name__)

#flask routes 

@app.route("/")
def root():
    """List all available API routes"""
    return (
        f"Available API routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"//api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session from python to db
    results = Session.query(Measurement.date, Measurement.prcp).all()
    Session.close()
    #convert results into list
    perc_data = list(np.ravel(results))
    return jsonify(perc_data)

# def stations():
# /api/v1.0/stations
# /api/v1.0/stations
# /api/v1.0/<start> and /api/v1.0/<start>/<end>



if __name__ == "__main__":
    app.run(debug=True)
