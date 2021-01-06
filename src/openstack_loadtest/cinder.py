import random

import locust

from openstack_loadtest import base


class CinderUser(base.OpenStackUser):
    volumes = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Turn this class into a singleton, so we populate the volumes list once."""
        if cls._instance is None:
            cls._instance = super(CinderUser, cls).__new__(cls)
            cls._instance._os_connection()
            cls._instance.volumes = cls._instance._get_volumes()
            cls._instance.snapshots = cls._instance._get_snapshots()
        return cls._instance

    def _get_volumes(self):
        """Limit the list to 10"""
        return list(self.openstack.volume.volumes(details=False))[:10]

    def _get_snapshots(self):
        """Limit the list to 10"""
        return list(self.openstack.volume.snapshots(details=False))[:10]

    def service_endpoint(self):
        return self.openstack.endpoint_for("volumev3")

    @locust.task
    @locust.tag("volumes")
    def volumes(self):
        self.client.get("/volumes", headers=self.openstack_headers)

    @locust.task
    @locust.tag("volumes_info")
    def volume_info(self):
        v = random.choice(self.volumes)
        self.client.get("/volumes/{}".format(v["id"]), headers=self.openstack_headers)

    @locust.task
    @locust.tag("snapshots")
    def snapshots(self):
        self.client.get("/snapshots", headers=self.openstack_headers)

    @locust.task
    @locust.tag("snapshots_info")
    def snapshot_info(self):
        if self.snapshots:
            s = random.choice(self.snapshots)
            if s:
                self.client.get("/snapshots/{}".format(s["id"]), headers=self.openstack_headers)
