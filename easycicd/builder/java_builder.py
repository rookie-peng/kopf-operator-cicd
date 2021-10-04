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
        tag = "registry.rootcloud.com/devops" + "/" + self.root_path.split("/")[1] + ":" + str(time.time()).split(".")[0]
        env = app_config(self.root_path)
        print("&&&&&&&&&&&&&&&&&&&&&, flag1")
        # with open("easycicd/builder/multi-stage-dockerfile/Dockerfile.java", "r") as fileobj:
        #     image, build_log = self.client.images.build(fileobj=fileobj, tag=tag, target='BUILD', rm=True)

        # 通过arg传入rootpath, 方便dockerfile做处理
        image, build_log = self.client.images.build(path='easycicd/builder/multi-stage-dockerfile/', dockerfile='Dockerfile.java', tag=tag, target='BUILD', rm=True)
        # image = "nginx:v1"
        print("image name is ------------------", image)
        # return image, env, build_log
        return image, env


