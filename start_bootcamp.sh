source ./py3envs/platform/bin/activate && cd platform && FLASK_APP=lti_platform.py flask run -h 0.0.0.0 &
source ./py3envs/notebook/bin/activate && \
cd notebook/notebooks && \
PYTHONPATH=$PYTHONPATH:/jupyterext jupyter notebook --allow-root --NotebookApp.nbserver_extensions="{'storeandshow.requesthandler':True}"

