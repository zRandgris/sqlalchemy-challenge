# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

#pathway might need to be changed for different file path! or move app.py into Resources!
engine = create_engine("sqlite:///Data Boot Camp\Module 10 Challenge\sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# # Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station


# Create our session (link) from Python to the DB

session = Session(engine)

# Data Boot Camp\Module 10 Challenge\sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():

    return(f'Temp')

##################################################################################################
## Data for Precipitation
recent_date, = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days = 366)
    
results = session.query(Measurement.date, Measurement.prcp).\
                  filter(Measurement.date > year_ago).all()
measure_data = [{"Date": result[0], "Precipitation": result[1]} for result in results]
##################################################################################################
##################################################################################################
## Data for stations
results2 = session.query(Measurement.station, func.count(Measurement.station)).\
                   group_by(Measurement.station).\
                   order_by(func.count(Measurement.station).desc()).all()
measure_data2 = [{"Station": result2[0], "Number of Station": result2[1]} for result2 in results2]
##################################################################################################
##################################################################################################
## Data for tobs
most_active_id = results2[0][0]

most_active_id

results3 = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station == most_active_id).\
        filter(Measurement.date >= year_ago).all()
measure_data3 = [{"Station": result3[0], "tobs": result3[1]} for result3 in results3]

##################################################################################################
################################# APP ROUTES #####################################################
#A precipitation route
@app.route("/precipitation")
def precipitation():

    
    return jsonify(measure_data)


##################################################################################################
#A stations route
@app.route("/stations")
def stations():
  
    
    return(measure_data2)

##################################################################################################
#A tobs route
@app.route("/tobs")
def tobs():

    return(measure_data3) 

##################################################################################################
#A start route

@app.route("/<start>")
def starts(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')    
    start_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).all()
    measure_data4 = [{"Ending Date is: ": recent_date,"min": data[0], "avg": data[1], "max": data[2], "Starting Date is: ": start_date} for data in start_data]
    return jsonify(measure_data4)
##################################################################################################
#A start/end route

@app.route("/<start>/<end>")
def start_end(start,end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    start_end_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    measure_data5 = [{"Ending Date is: ": end_date,"min": data[0], "avg": data[1], "max": data[2], "Starting Date is: ": start_date} for data in start_end_data]
    return jsonify(measure_data5)


##################################################################################################
# Closing session
session.close()

if __name__ == "__main__":
    app.run(debug=True)
