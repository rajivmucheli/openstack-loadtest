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

    @locust.task
    @locust.tag("user_info")
    def user_info(self):
        v = random.choice(self.users)
        if v:
            self.client.get("/users/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("domains")
    def domains(self):
        self.client.get("/domains", headers=self.openstack_headers)

    @locust.task
    @locust.tag("domain_info")
    def domain_info(self):
        v = random.choice(self.domains)
        if v:
            self.client.get("/domains/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("roles")
    def roles(self):
        self.client.get("/roles", headers=self.openstack_headers)

    @locust.task
    @locust.tag("role_info")
    def role_info(self):
        v = random.choice(self.roles)
        if v:
            self.client.get("/roles/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("policies")
    def policies(self):
        self.client.get("/policies", headers=self.openstack_headers)

    @locust.task
    @locust.tag("policy_info")
    def policy_info(self):
        v = random.choice(self.policies)
       Continuing from the previous response:

```python
        if v:
            self.client.get("/policies/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("services")
    def services(self):
        self.client.get("/services", headers=self.openstack_headers)

    @locust.task
    @locust.tag("service_info")
    def service_info(self):
        v = random.choice(self.services)
        if v:
            self.client.get("/services/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("endpoints")
    def endpoints(self):
        self.client.get("/endpoints", headers=self.openstack_headers)

    @locust.task
    @locust.tag("endpoint_info")
    def endpoint_info(self):
        v = random.choice(self.endpoints)
        if v:
            self.client.get("/endpoints/{}".format(v["id"]), headers=self.openstack_headers)
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
    @locust.tag("create_credential")
    def create_credential(self):
        credential_data = {
            "credential": {
                "type": "ec2",
                "blob": "dummy-blob",
                "user_id": random.choice(self.users)["id"]
            }
        }
        self.client.post("/credentials", json=credential_data, headers=self.openstack_headers)

    @locust.task
    @locust.tag("update_credential")
    def update_credential(self):
        v = random.choice(self.credentials)
        if v:
            credential_data = {
                "credential": {
                    "blob": "updated-blob"
                }
            }
            self.client.patch("/credentials/{}".format(v["id"]), json=credential_data, headers=self.openstack_headers)

    @locust.task
    @locust.tag("delete_credential")
    def delete_credential(self):
        v = random.choice(self.credentials)
        if v:
            self.client.delete("/credentials/{}".format(v["id"]), headers=self.openstack_headers)
