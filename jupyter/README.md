# Running Jupyter with the required dependencies

1. cd to this directory
1. Create a virtual env: python3 -m venv /path/to/new/virtual/environment
2. Activate your virtual env: source /path/to/new/virtual/environment/bin/activate 
3. run: pip install -r requirements.txt

To run the notebook locally: jupyter notebook. Your browser should open.

# OIDC Call back support

To enable the OIDC response to populate the Kernel, the notebook to be run with the custom extension handler (see jupterext/storeandshow).

To run with that extension: 

add path to PYTHON_PATH env, for example:
export PYTHONPATH=$PYTHONPATH:/home/claude/projects/lti_bootcamp/jupyterext

then run the notebook activating this extension:
jupyter notebook --NotebookApp.nbserver_extensions="{'storeandshow.requesthandler':True}"
                                                                                                                 
or:

PYTHONPATH=$PYTHONPATH:/home/claude/projects/lti_bootcamp/jupyterext jupyter notebook --NotebookApp.nbserver_extensions="{'storeandshow.requesthandler':True}"