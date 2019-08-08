import numpy as np
import datetime as dt
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB


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
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"<br/>"
        f"/api/v1.0/<start> <br/>"
        f"<br/>  "
        f"Use a Start Date, Example: 2016-12-31"
        f"<br/>   "
        f"/api/v1.0/<start>/<end> <br/>"
        f"<br/>"
        f"Use a Start Date and and End Date seperated by / "

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #query all dates and prcp
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    #create a list to append results to 
    precipitation = []
    # Create a dictionary from the row data and append to a list of precipitation
    for date, pcrp in results:
        precipitation_dict = {} 
        precipitation_dict["date"] = date 
        precipitation_dict["pcrp"] = pcrp 
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    #query station data, stations 
    session = Session(engine)
    results = session.query(station.station).all()
    # Convert list of tuples into normal list 
    all_stations = list(np.ravel(results))
    #jsonify the list and return 
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def Tobs():
    #variables for beginning and end of 12 month time frame 
    Beg = dt.datetime(2016,8,23) 
    End = dt.datetime(2017,8,24)
    # Design a query to pull date and tobs values for previous year (last 12 months)

    session = Session(engine)
    #query date and tobs from measurements, and filter(WHERE) date is between beggining and end of year
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > Beg).filter(measurement.date < End).all()
    #query tobs from measurements between beggining and end of year
    results2 = session.query(measurement.tobs).\
    filter(measurement.date > Beg).filter(measurement.date < End).all()
    #create a list to append results to  
    previous_year = []
    #Create a dictionary from the row data and append to a list of previous_year
    for date, tobs in results:

        previous_year_dict = {}
        previous_year_dict["date"] = date
        previous_year_dict["tobs"] = tobs
        previous_year.append(previous_year_dict)
    
    # Convert list of tuples into normal list
    prev_year = list(np.ravel(results2)) 

    return jsonify(prev_year, previous_year)



@app.route("/api/v1.0/<start>")
def trip1(start):
    session = Session(engine)
    # create variable start date and time delta one year prior for last year   
    start_date = dt.datetime.strptime(start, '%Y-%m-%d') 
    last_year = dt.timedelta(days=365)
    #start variable with one year arithmatic 
    start = start_date-last_year
    #end date
    end =  dt.date(2017, 8, 23)
    #query minimum tobs, average tobs and max tobs from measurements and filter(WHERE) date is between start variable and end of year
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    #Convert list of tuples into a normal list 
    trip = list(np.ravel(trip_data))

    return jsonify(trip) 


@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):
    session = Session(engine)
     #Create a variable start and end dates, and time delta one year back for last year 
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    #start variable with one year arithmatic
    start = start_date-last_year
    #end date with one year arithmatic, so that the inputs are between start and end date
    end = end_date-last_year
    #query minimum tobs, average tobs, and maximum tobs from measurements and filter (WHERE) between start and end dates variables entered in path 
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    #Convert list of tuples into a normal list 
    trip = list(np.ravel(trip_data))
    return jsonify(trip)   









    
     

    




























if __name__ == '__main__':
        app.run(debug=True)