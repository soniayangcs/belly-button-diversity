import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)

# Save reference to the tables
OTU = Base.classes.otu
Samples = Base.classes.samples
Samples_metadata = Base.classes.samples_metadata


@app.route("/")
def home():
    # Return the dashboard homepage.
    return render_template("index.html")


@app.route('/names')
def names():
    #List of sample names.

    """Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]"""
    
    sampleIDs = Samples.__table__.columns
    
    sampleID_list = []
    
    for sampleID in sampleIDs:
        sampleID_list.append(sampleID.key)
    
    return jsonify(sampleID_list)
    

@app.route('/otu')
def otu():
    """List of OTU descriptions.

    Returns a list of OTU descriptions in the following format

    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """
    
    otu_descriptions = session.query(OTU.lowest_taxonomic_unit_found).all()
    
    otu_descriptions_list = []
    
    for otu_description in otu_descriptions:
        otu_descriptions_list.append(otu_description[0])
    
    return jsonify(otu_descriptions_list)
    
@app.route('/metadata/<sample>')
def sample_metadata(sample):
    """MetaData for a given sample.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
    
    #database stores the ID's without BB so we need to remove that
    #and convert the number to an int
    temp = sample.replace("BB_", "")
    sample_number = int(temp)
    
    #query database for the info we need 
    results = session.query(Samples_metadata.AGE, Samples_metadata.BBTYPE,
                             Samples_metadata.ETHNICITY, Samples_metadata.GENDER, Samples_metadata.LOCATION, Samples_metadata.SAMPLEID).filter_by(SAMPLEID = sample_number).all()
    
    BB_sample = {'AGE: ': results[0][0],
                 'BBTYPE: ': results[0][1],
                 'ETHNICITY: ': results[0][2],
                 'GENDER: ': results[0][3],
                 'LOCATION: ': results[0][4],
                 'SAMPLEID: ': results[0][5]
                 }
    
    return jsonify(BB_sample)
    
@app.route('/wfreq/<sample>')
def wfreq(sample):
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns an integer value for the weekly washing frequency `WFREQ`
    """

    #database stores the ID's without BB so we need to remove that
    #and convert the number to an int
    temp = sample.replace("BB_", "")
    sample_number = int(temp)
    
    results = session.query(Samples_metadata.WFREQ).filter_by(SAMPLEID = sample_number).all()
    
    wfreq = results[0][0]
    
    return jsonify(wfreq)
    
    
@app.route('/samples/<sample>')
def otu_and_samples(sample):
    """OTU IDs and Sample Values for a given sample.

    Sort your Pandas DataFrame (OTU ID and Sample Value)
    in Descending Order by Sample Value

    Return a list of dictionaries containing sorted lists  for `otu_ids`
    and `sample_values`

    [
        {
            otu_ids: [
                1166,
                2858,
                481,
                ...
            ],
            sample_values: [
                163,
                126,
                113,
                ...
            ]
        }
    ]"""
    
    results = session.query(Samples).filter(getattr(Samples, sample)) \
              .order_by(getattr(Samples, sample).desc()).all()
              
    otu_ids = []
    sample_values = []
    
    for row in results:
        otu_ids.append(row.otu_id)
        sample_values.append(getattr(row,sample))
        
    return jsonify([{'otu_ids': otu_ids,
                     'sample_values': sample_values}])

if __name__ == "__main__":
    app.run(debug=True)