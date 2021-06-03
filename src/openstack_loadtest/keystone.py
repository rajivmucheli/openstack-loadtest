import random
import locust
from openstack_loadtest import base

class KeystoneUser(base.OpenStackUser):
    projects = None
    _instance = None
    def __new__(cls, *args, **kwargs):
        """Turn this class into a singleton, so we populate the projects list once."""
        if cls._instance is None:
            cls._instance = super(KeystoneUser, cls).__new__(cls)
            cls._instance._os_connection()
            cls._instance.projects = cls._instance._get_projects()
            cls._instance.credentials = cls._instance._get_credentials()
            cls._instance.users = cls._instance._get_users()
        return cls._instance

    def _get_projects(self):
        """Limit the list to 10"""
        return list(self.openstack.identity.projects())

    def _get_credentials(self):
        """Limit the list to 10"""
        return list(self.openstack.identity.credentials())     

    def _get_users(self):
        """Limit the list to 10"""
        return list(self.openstack.identity.users()) 
        
    def service_endpoint(self):
        return self.openstack.endpoint_for("identity")

    @locust.task
    @locust.tag("projects")
    def projects(self):
        self.client.get("/projects", headers=self.openstack_headers)

    @locust.task
    @locust.tag("project_info")
    def project_info(self):
        v = random.choice(self.projects)
        if v:
            self.client.get("/projects/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("credentials")
    def credentials(self):
        self.client.get("/credentials", headers=self.openstack_headers)

    @locust.task
    @locust.tag("credentials_info")
    def credentials_info(self):
        v = random.choice(self.credentials)
        if v:
            self.client.get("/credentials/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("users")
    def users(self):
        self.client.get("/users", headers=self.openstack_headers)