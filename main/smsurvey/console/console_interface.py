import json

from tornado.web import RequestHandler

from smsurvey.core.security import secure
from smsurvey.core.services.owner_service import OwnerService
from smsurvey.core.services.plugin_service import PluginService


class PluginsRequestHandler(RequestHandler):

    def get(self):
        session_id = self.get_argument("session_id")

        owner_id = secure.get_session_owner_id(session_id)
        owner = OwnerService.get_by_id(owner_id)

        p = PluginService.get_by_owner_id(owner.id)

        plugins = []

        for plugin in p:
            plugins.append({
                'name': plugin.name,
                'url': plugin.url,
                'icon': plugin.icon
            })

        response = {
            "status": "success",
            "plugins": plugins
        }

        self.write(json.dumps(response))
        self.flush()

    def data_received(self, chunk):
        pass