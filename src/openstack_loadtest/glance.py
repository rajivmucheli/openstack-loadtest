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

    # New Glance API tasks

    @locust.task
    @locust.tag("image_upload")
    def upload_image(self):
        # Replace `<path_to_image>` with the actual path to the image file you want to upload
        with open("<path_to_image>", "rb") as image_file:
            self.client.post(
                "/v2/images",
                data=image_file,
                headers=self.openstack_headers,
                name="Upload Image",
            )

    @locust.task
    @locust.tag("image_delete")
    def delete_image(self):
        v = random.choice(self.images)
        if v:
            self.client.delete(
                "/v2/images/{}".format(v["id"]),
                headers=self.openstack_headers,
                name="Delete Image",
            )

    @locust.task
    @locust.tag("image_schema")
    def image_schema(self):
        self.client.get("/v2/schemas/image", headers=self.openstack_headers, name="Image Schema")

    # New Glance Image Tasks API tasks

    @locust.task
    @locust.tag("image_tasks")
    def image_tasks(self):
        self.client.get("/v2/tasks", headers=self.openstack_headers, name="Image Tasks")

    @locust.task
    @locust.tag("image_task_info")
    def image_task_info(self):
        tasks = self.client.get("/v2/tasks", headers=self.openstack_headers).json()
        if tasks:
            task = random.choice(tasks)
            self.client.get(
                "/v2/tasks/{}".format(task["id"]),
                headers=self.openstack_headers,
                name="Image Task Info",
            )

    # Add more Glance API tasks as needed

