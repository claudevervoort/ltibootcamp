To install see https://jupyterhub.readthedocs.io/en/stable/quickstart.html

jupyter requirements.txt includes the python Jupyter Hub dependencies.

clear users:
 getent passwd | awk -F: '{ print $1 }' | grep ltibc | xargs -L 1 sudo userdel -r

start jupyterhub systemd spawner: start_jh_systemd.sh


