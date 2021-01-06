import abc
import os

import locust
import openstack
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OpenStackUser(locust.HttpUser):
    # The openstack connection object
    openstack = None

    def __init__(self, *args, **kwargs):
        self._os_connection()
        self.host = self.service_endpoint()
        super(OpenStackUser, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def service_endpoint(self):
        """Return the endpoint for the openstack service."""
        # step 1: know the service endpoint's name in keystone
        # For example, cinder is 'volumev3'
        # step 2: return self.openstack.endpoint_for("volumev3")
        pass

    def _os_connection(self):
        cloud_name = os.getenv("OS_CLOUD")
        if not cloud_name:
            raise Exception("Must set environment var OS_CLOUD")

        try:
            self.openstack = openstack.connect(cloud=cloud_name)
            self.openstack.authorize()
            self.openstack_headers = self.openstack.session.get_auth_headers(
                self.openstack.session.auth
            )
        except Exception as ex:
            raise ex
