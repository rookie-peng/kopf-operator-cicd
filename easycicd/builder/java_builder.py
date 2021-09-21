import os
import time
from .base_builder import BuilderBase
from easycicd.operation.resource_configmap import app_config


class Builder(BuilderBase):
    def __init__(self, url, root_path, gitbranch):
        super(Builder, self).__init__(url, root_path, gitbranch)

    def builder(self):
        # tag = url/repo_name/app_name: timestamp
        # tag = os.environ.get("registry") + "/" + self.root_path.split("/")[1] + ":" + str(time.time()).split(".")[0]
        tag = "registry.rootcloud.com/devops" + "/" + "self.root_path.split("/")[1]" + ":" + str(time.time()).split(".")[0]
        env = app_config(self.root_path)

        with open("multi-stage-dockerfile/Dockerfile.java", "r") as fileobj:
            image, build_log = self.client.images.build(fileobj=fileobj, tag=tag, target='BUILD', rm=True)

        return image, env, build_log


