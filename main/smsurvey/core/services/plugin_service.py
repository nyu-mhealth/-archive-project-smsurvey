import json
import os
import time
from base64 import b64encode

import requests

from smsurvey.core.model.model import Model
from smsurvey.core.model.query.where import Where

from smsurvey.core.security import secure
from smsurvey.core.services.owner_service import OwnerService


class PluginService:

    @staticmethod
    def get_plugin(plugin_id):
        plugins = Model.repository.plugins
        return plugins.select(Where(plugins.id, Where.EQUAL, plugin_id))

    @staticmethod
    def get_by_owner_id(owner_id):
        plugins = Model.repository.plugins
        return plugins.select(Where(plugins.owner_id, Where.E, owner_id), force_list=True)

    @staticmethod
    def validate_plugin(plugin_id, owner_name, owner_domain, token):
        plugin = PluginService.get_plugin(plugin_id)

        if plugin is not None:
            owner = OwnerService.get_by_id(plugin.owner_id)
            if owner_name == owner.name and owner_domain == owner.domain:
                test = secure.encrypt_password(token, plugin.salt).decode()
                return test == plugin.secret_token

        return False

    @staticmethod
    def is_owned_by(plugin_id, owner_id):
        plugin = PluginService.get_plugin(plugin_id)

        if plugin is None:
            return False

        return plugin.owner_id == owner_id

    @staticmethod
    def is_plugin_registered(plugin_id):
        return PluginService.get_plugin(plugin_id) is not None

    @staticmethod
    def register_plugin(name, owner_id, url, icon, permissions):

        token = secure.encrypt_password(owner_id + str(time.time())).decode()
        salt_for_token = b64encode(os.urandom(16)).decode()
        salted_token = secure.encrypt_password(token, salt_for_token).decode()

        plugins = Model.repository.plugins
        plugin = plugins.create()

        plugin.name = name
        plugin.owner_id = owner_id
        plugin.secret_token = salted_token
        plugin.salt = salt_for_token
        plugin.permissions = permissions
        plugin.icon = icon
        plugin.url = url

        return plugin.save(), token

    @staticmethod
    def delete_plugin(plugin_id):
        plugins = Model.repository.plugins
        plugins.delete(Where(plugins.id, Where.E, plugin_id))

    @staticmethod
    def poke(plugin_id, survey_id):
        plugin = PluginService.get_plugin(plugin_id)

        data = {
            'plugin_id': plugin_id,
            'survey_id': survey_id
        }

        requests.post(plugin.url + "/poke", json.dumps(data))