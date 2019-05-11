from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import json
import os
from jupyter_client import KernelClient, BlockingKernelClient
from tornado import template
import tornado


class ConnectionInfoHandler(IPythonHandler):

    clients_by_id = {}
    
    def create_kernel_client(self, ci):
        kernel_client = BlockingKernelClient()
        kernel_client.load_connection_info(ci)
        kernel_client.start_channels(shell=True, iopub=False, stdin=False, hb=False)
        return kernel_client
    
    def post(self):
        ci = tornado.escape.json_decode(self.request.body)

        if ci['id'] and ci['ci']:
            if not ci['id'] in ConnectionInfoHandler.clients_by_id:
                ConnectionInfoHandler.clients_by_id[ci['id']] = self.create_kernel_client(ci['ci'])
                client = ConnectionInfoHandler.clients_by_id[ci['id']]
                client.execute("connect_id='{0}';".format(ci['id']))
                self.finish('Registered {0}'.format(ci['id']))
            else:
                self.finish('Already registered {0}'.format(ci['id']))
        else:
            self.set_status(400)
            self.finish('Missing params')

    def check_xsrf_cookie(self):
        pass

class PingHandler(IPythonHandler):

    def get(self):
        self.finish('pong!')

class SetAndShowHandler(IPythonHandler):

    def post(self):
        if not self.logged_in:
            self.set_status(401)
            self.finish('')
            return
        id_token = self.get_body_argument('id_token')
        state = self.get_body_argument('state')
        ci_id = self.get_query_argument('ciid', None)
        if ci_id and ci_id in ConnectionInfoHandler.clients_by_id:
            client = ConnectionInfoHandler.clients_by_id[ci_id] 
            # should be neutralized or use a custom IPython extension?
            # but fine for the context of the LTI bootcamp notebook
            code = "id_token='{0}';state='{1}'".format(id_token, state)
            client.execute(code)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        loader = template.Loader(dir_path)
        self.finish(loader.load("authresponse.html").generate(state=state, id_token=id_token))

    def check_xsrf_cookie(self):
        pass

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/setandshow')
    web_app.add_handlers(host_pattern, [(route_pattern, SetAndShowHandler)])
    route_pattern = url_path_join(web_app.settings['base_url'], '/auth')
    web_app.add_handlers(host_pattern, [(route_pattern, SetAndShowHandler)])
    route_pattern_r = url_path_join(web_app.settings['base_url'], '/setci')
    web_app.add_handlers(host_pattern, [(route_pattern_r, ConnectionInfoHandler)])
    route_pattern_r = url_path_join(web_app.settings['base_url'], '/ping')
    web_app.add_handlers(host_pattern, [(route_pattern_r, PingHandler)])

    print("store_and_show handler added, set ci route is {0}".format(route_pattern_r))
