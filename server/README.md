# LTI Bootcamp supporting server

A simple in memory platform used to exercise the various API and messages of the LTI Advantage
under a 1.3 integration.

# Install and Run

1. cd to this directory
1. Create a virtual env: python3 -m venv /path/to/new/virtual/environment
2. Activate your virtual env: source /path/to/new/virtual/environment/bin/activate 
3. run: pip install -r requirements.txt

Then to run: FLASK_APP=lti_platform.py flask run

# Docker to run server

Build a docker image using the provided Dockerfile:

    docker build -t lti-1-dot-3-consumer .

Then run the image in a new container. 

    docker run -d -e FLASK_APP=lti_platform.py -p 5000:5000 -t lti-1-dot-3-consumer 

open the hello page at: http://localhost:5000/




