import random
import locust
from openstack_loadtest import base
class BarbicanUser(base.OpenStackUser):
    secrets = None
    _instance = None
    def __new__(cls, *args, **kwargs):
        """Turn this class into a singleton, so we populate the secrets list once."""
        if cls._instance is None:
            cls._instance = super(BarbicanUser, cls).__new__(cls)
            cls._instance._os_connection()
            cls._instance.secrets = cls._instance._get_secrets()
        return cls._instance
    def _get_secrets(self):
        """Limit the list to 10"""
        return list(self.openstack.key_manager.secrets())[:10]
    def service_endpoint(self):
        return self.openstack.endpoint_for("key-manager")
    @locust.task
    @locust.tag("secrets")
    def secrets(self):
        self.client.get("/v1/secrets", headers=self.openstack_headers)
    @locust.task
    @locust.tag("secrets_info")
    def secret_info(self):
        v = random.choice(self.secrets)
        secret_uuid = v["id"].rstrip('/').rsplit('/', 1)
        self.client.get("/v1/secrets/{}".format(secret_uuid[-1]), headers=self.openstack_headers)
