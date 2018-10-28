from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import json
from jupyter_client import KernelClient, BlockingKernelClient

class ConnectionInfoHandler(IPythonHandler):

    clients_by_id = {}
    
    def create_kernel_client(self, ci):
        kernel_client = BlockingKernelClient()
        kernel_client.load_connection_info(ci)
        kernel_client.start_channels()
        return kernel_client
    
    def post(self):
        if not self.logged_in:
            self.set_status(401)
            self.finish('')
            return
        id = self.get_body_argument('id')
        connection_info = self.get_body_argument('ci')
        if id and connection_info:
            if not id in ConnectionInfoHandler.clients_by_id:
                ci = json.loads(connection_info)
                ConnectionInfoHandler.clients_by_id[id] = self.create_kernel_client(ci)
                self.finish('Registered')
            else:
                self.finish('Already registered')
        else:
            self.set_status(400)
            self.finish('Missing params, id or ci')

    def check_xsrf_cookie(self):
        pass

class SetAndShowHandler(IPythonHandler):

    def post(self):
        if not self.logged_in:
            self.set_status(401)
            self.finish('')
            return
        id_token = self.get_body_argument('id_token')
        state = self.get_body_argument('state')
        ci_id = self.get_query_argument('ciid')
        if ci_id and state and id_token and ci_id in ConnectionInfoHandler.clients_by_id:
            client = ConnectionInfoHandler.clients_by_id[ci_id] 
            # should be neutralized or use a custom IPython extension?
            # but fine for the context of the LTI bootcamp notebook
            code = "id_token='{0}';state='{1}'".format(id_token, state)
            client.start_channels
            client.execute(code)
            self.finish('state and id_token received')
        else:
            self.set_status(400)
            self.finish('Missing parameters or not configured client')

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
    route_pattern_r = url_path_join(web_app.settings['base_url'], '/setci')
    web_app.add_handlers(host_pattern, [(route_pattern_r, ConnectionInfoHandler)])
