# eventually break bootcamp in dedicated repos - or get fancy about listing the files to download one by one
curl -s https://codeload.github.com/claudevervoort-perso/ltibootcamp/zip/master -o ltibootcamp.zip
unzip -o -qq ltibootcamp.zip

# so that users can add their own books by dupllicating the master
chmod a+rwx ltibootcamp-master/jupyter/notebooks

jupyterhub