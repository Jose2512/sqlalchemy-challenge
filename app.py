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

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date <= "2017-08-23").\
    filter(Measurement.date >= "2016-08-23").all()

    session.close()

    precipitate = []
    for date, prcp in results:
        prec_dict = {}
        prec_dict["name"] = date
        prec_dict["prcp"] = prcp
        precipitate.append(prec_dict)
        
    return jsonify(precipitate)




if __name__ == "__main__":
    app.run(debug=True)