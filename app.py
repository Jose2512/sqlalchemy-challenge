import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>"
    )
#################### precipitation Page ####################

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_str = str(last_date[0]).split("-")
    last_date_dt = dt.date(int(last_date_str[0]),int(last_date_str[1]),int(last_date_str[2]))
    last_date_dt
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date <= last_date_dt).\
    filter(Measurement.date >= (last_date_dt-dt.timedelta(days=365))).all()
    session.close()
    precipitate = []
    for date, prcp in results:
        prec_dict = {}
        prec_dict["name"] = date
        prec_dict["prcp"] = prcp
        precipitate.append(prec_dict)    
    return jsonify(precipitate)

#################### Stations Page ####################
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).\
    session.close()
    stations = []
    for station, name, latitude, longitude, altitude in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["altitude"] = altitude
        stations.append(station_dict)
        
    return jsonify(stations)
#################### Temperature Obsdervations Page ####################

@app.route("/api/v1.0/<start>")
def tobs_one_date(start):
    session = Session(engine)
    tobs_last12 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    tobs_m_m_a = []
    for min, max, avg in results:
        tobs_mma_dict = {}
        tobs_mma_dict["min"] = min
        tobs_mma_dict["max"] = max
        tobs_mma_dict["avg"] = avg
        tobs_m_m_a.append(tobs_dict)    
    return jsonify(tobs_m_m_a)

#################### precipitation Page ####################







if __name__ == "__main__":
    app.run(debug=True)