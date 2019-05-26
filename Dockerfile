FROM python:latest

ADD ./server/ /platform
ADD ./jupyter /notebook
ADD ./jupyterext /jupyterext

RUN mkdir py3envs && mkdir py3envs/platform \
&& python3 -m venv ./py3envs/platform \
&& . ./py3envs/platform/bin/activate \
&& pip install -r ./platform/requirements.txt

RUN mkdir py3envs/notebook \
&& python3 -m venv ./py3envs/notebook \
&& . ./py3envs/notebook/bin/activate \
&& pip install -r ./notebook/requirements.txt \
&& jupyter notebook --generate-config

RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py \
&& echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py

ADD ./start_bootcamp.sh start_bootcamp.sh

EXPOSE 5000
EXPOSE 8888

CMD ["/bin/bash", "./start_bootcamp.sh"]
