# LTI Bootcamp

Text and code together to learn how to use LTI 1.3 advantage

LTI Bootcamp has 2 components:

- Server: an LTI platform simulator, implementing most of LTI 1.3 Advantage
- Jupyter Notebook: A Jupyter notebook to simulate a Tool interacting with a platform

# Docker to run server

Build a docker image using the provided Dockerfile:

    docker build -t lti-1-dot-3-consumer .

Then run the image in a new container. 

    docker run -d -e FLASK_APP=lti_platform.py -p 5000:5000 -t lti-1-dot-3-consumer 

open the hello page at: http://localhost:5000/

