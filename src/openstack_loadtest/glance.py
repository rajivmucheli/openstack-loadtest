import random
import locust
from openstack_loadtest import base
class GlanceUser(base.OpenStackUser):
    images = None
    _instance = None
    def __new__(cls, *args, **kwargs):
        """Turn this class into a singleton, so we populate the images list once."""
        if cls._instance is None:
            cls._instance = super(GlanceUser, cls).__new__(cls)
            cls._instance._os_connection()
            cls._instance.images = cls._instance._get_images()
        return cls._instance
    def _get_images(self):
        """Limit the list to 10"""
        return list(self.openstack.image.images())[:10]
    def service_endpoint(self):
        return self.openstack.endpoint_for("image")
    @locust.task
    @locust.tag("images")
    def images(self):
        self.client.get("/v2/images", headers=self.openstack_headers)
    @locust.task
    @locust.tag("images_info")
    def image_info(self):
        v = random.choice(self.images)
        if v:
            self.client.get("/v2/images/{}".format(v["id"]), headers=self.openstack_headers)