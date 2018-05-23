<img src="jupyter/notebooks/assets/bootcamp.png">

# LTI Bootcamp

Text and code together to learn how to use LTI 1.3 advantage

LTI Bootcamp has 2 components:

- Server: an LTI platform simulator, implementing most of LTI 1.3 Advantage
- Jupyter Notebook: A Jupyter notebook to simulate a Tool interacting with a platform

<img src="jupyter/notebooks/assets/bootcamp_arch.png">

# Limitation of the bootcamp

The bootcamp uses Jupyter to mix live code and text. Since the platform cannot launch into Jupyter, the bootcamp LTI server has API to get launch data (the data a tool would normatlly receive in the launch POST request).

# How to use

Once you have the notebook and the server up, open the ltibootcamp notebook, and enter the server URL where prompted. Then follow the book...

# Virtual Env

With Python3 around, you can easily run the bootcamp:

You can run the jupyter notebook and the lti server in 2 virtual envs.
See [Jupyter README](jupyter/README.md) and [Server README](server/README.md).

The server URL is going to be: http://localhost:5000 . Verify it runs. Jupyter should have opened in your browser, so just need to navigate to the notebook.

# Docker - not totally working

If you have docker installed, you might prefer to go the docker road. A bit heavier but arguably simpler:

Cd in this folder, and run docker-compose up. 1st run? Wait a bit... and more... until the internet is downloaded. Then you should be good to go.

You need to use the http://platform:5000 for the platform URL. Later in the notebook, the notebook makes a browser request to that URL (displaying the response of the content item), and that won work. Either change that url to localhost, add platform 127.0.0.1 to your host or play with extra_hosts (https://biancatamayo.me/blog/2017/11/03/docker-add-host-ip/).