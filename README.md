
# set up a clean environment


```
python3 -m venv ~/.dash10
source ~/.dash10/bin/activate
pip install dash
pip install dash_bootstrap_components
pip install requests
pip install pandas
pip freeze > requirements.txt
```

# Colorado Congressional Map for IX Power
# Dash App to display static html map (folium) and find lat/lon from address field.
# if address is found, a mapbox street map is presented to user to verify #results
# api calls to google for address geocoding
# api call to our geoservice running on app runner to identify what district #user is in
# single page app with routing defined.


This has been moved to app runner using github. 

See:  https://www.coursera.org/learn/cloud-machine-learning-engineering-mlops-duke/lecture/FOjTX/continuously-deploy-flask-ml-application

use the github method, not containers - ecr.

#  from here:

https://github.com/russellromney/docker-dash/blob/master/README.md


