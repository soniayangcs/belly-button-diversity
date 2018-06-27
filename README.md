# Belly Button Biodiversity
* An interactive dashboard to explore the Belly Button Biodiversity DataSet (http://robdunnlab.com/projects/belly-button-biodiversity/).

### Flask API

* API for dataset and to serve the HTML
* connects to a sqlite database file
* Flask app has routes that routes that return the dashboard homepage, a list of sample names ('/names'), a list of OTU descriptions ('/otu'), metadata for a given sample ('/metadata/<sample>'), weekly washing frequency for a given sample ('/wfreq/<sample>'), & OTU IDs and Sample Values for a given sample ('/samples/<sample>').


### Plotly.js

* Uses the route /names (from the Flask app) to populate a dropdown select element with the list of sample names

* Has a function called optionChanged to handle the change event when a new sample is selected (i.e. fetch data for the newly selected sample).

* Creates a PIE chart that uses data from routes /samples/<sample> and /otu to display the top 10 samples.

* Generates a simple metadata text table

* there are a few bugs (Plotly.restyle wasn't working for whatever reason, so I just redrew the new plot each time in the code)