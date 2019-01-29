FROM jupyterhub/jupyterhub:latest

RUN apt-get -qy update && apt-get -qy install unzip
RUN  curl -s https://raw.githubusercontent.com/claudevervoort-perso/ltibootcamp/master/jupyter/requirements.txt | sed -e 's/==/>=/' > ltibcreq.txt \
     && pip install -q -r ltibcreq.txt

ADD ./jupyterhub_config.py .
ADD ./get_notebooks_and_start.sh .

CMD /bin/bash get_notebooks_and_start.sh 