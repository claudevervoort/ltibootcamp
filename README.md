# LTI Bootcamp

Nothing to see here for now! Still being built up...

Build a docker image using the provided Dockerfile:

    docker build -t lti-1-dot-3-consumer .

Then run the image in a new container. 

    docker run -d -e FLASK_APP=lti_platform.py -p 5000:5000 -t lti-1-dot-3-consumer 

open the hello page at: http://localhost:5000/
