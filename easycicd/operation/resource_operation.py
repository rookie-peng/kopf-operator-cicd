import json
import os
import re
import kopf
import yaml
import requests
from kubernetes import client
from .rewrite_patch import AppsV2Api
from .resource_configmap import app_config
from easycicd.builder import base_builder, go_builder, java_builder, nodejs_builder, python_builder


@kopf.on.create('EasyCicd')
def create_fn(spec, name, namespace, logger, **kwargs):
    repo = spec.get('gitrepo')
    gitbranch = spec.get('gitbranch')
    type = spec.get('type')
    replicas = spec.get('replicas')
    labels = {'app': name, 'superpeng': 'easycicd', 'branch': gitbranch}  # 不区分数据类型，都要加引号

    # 拆分url，分成两部分
    m = re.search('(https?://[A-Za-z_0-9.-]+)/(.*)', repo)
    url = m.group(1)
    root_path = m.group(2)

    # 根据type判断代码语言，从而调用不同的builder，并使用eval使字符串变为可调用对象
    fun = eval(f"{type}_builder").Builder(url=url, root_path=root_path, gitbranch=gitbranch)

    # CI部分，处理代码下载，返回镜像和环境变量.
    # ci = base_builder.BuilderBase(url=url, root_path=root_path, gitbranch=gitbranch)
    # ci.start_get()
    # image = "busybox:latest"
    # env = app_config(root_path)

    # image, env, build_log = fun.builder()
    image, env = fun.builder()
    print("------------image", image)
    print("------------env", env)

    # path = os.path.join(os.path.dirname(__file__), 'deploy.yaml')
    # with open(path, 'rt') as f:
    #     tmpl = f.read()
    # text = tmpl.format(name=name, namespace=namespace, replicas=replicas, env=env, image=image, app=labels['app'], branch=labels['branch'], superpeng=labels['superpeng'])
    # body = yaml.safe_load(text)

    apps_api = client.AppsV1Api()
    body = client.V1Deployment(
                api_version="apps/v1",
                kind="Deployment",
                metadata=client.V1ObjectMeta(name=name),
                spec=client.V1DeploymentSpec(
                    replicas=replicas,
                    selector={'matchLabels': labels},
                    template=client.V1PodTemplateSpec(
                        metadata=client.V1ObjectMeta(labels=labels),
                        spec=client.V1PodSpec(
                            containers=[client.V1Container(
                                name=name,
                                image=image,
                                env=env,
                            )]
                        )
                    ),
                )
            )
    logger.info(f"{body}")

    # 使其成为子资源, 可以做到cr级联删除的效果
    kopf.adopt(body)

    try:
        apps_api.create_namespaced_deployment(
            namespace=namespace,
            body=body
        )
        logger.info(f"deployment is created: {name}")
    except Exception as e:
        status = getattr(e, "status")
        if status == 400:
            print(e)
            print("格式错误")
        elif status == 403:
            print("没权限")
    return {'deployment': name, 'author': 'superpeng'}


@kopf.on.update('EasyCicd')
def update_fn(spec, name, namespace, logger, **kwargs):
    repo = spec.get('gitrepo')
    gitbranch = spec.get('gitbranch')
    type = spec.get('type')
    replicas = spec.get('replicas')
    labels = {'app': name, 'superpeng': 'easycicd', 'branch': gitbranch}  # 不区分数据类型，都要加引号
    # image = "nginx:latest"
    import random
    # image = "mysql:5.7"
    ranint = random.randint(1, 50)
    image = f"mysql:{ranint}"
    env = [{"name": "age", "value": '18'}]

    # path = os.path.join(os.path.dirname(__file__), 'deploy.yaml')
    # with open(path, 'rt') as f:
    #     tmpl = f.read()
    # text = tmpl.format(name=name, namespace=namespace, replicas=replicas, env=env, image=image, app=labels['app'], branch=labels['branch'], superpeng=labels['superpeng'])
    # body = yaml.safe_load(text)

    apps_api = client.AppsV1Api()
    body = client.V1Deployment(
                api_version="apps/v1",
                kind="Deployment",
                metadata=client.V1ObjectMeta(name=name),
                spec=client.V1DeploymentSpec(
                    replicas=replicas,
                    selector={'matchLabels': labels},
                    template=client.V1PodTemplateSpec(
                        metadata=client.V1ObjectMeta(labels=labels),
                        spec=client.V1PodSpec(
                            containers=[client.V1Container(
                                name=name,
                                image=image,
                                env=env,
                            )]
                        )
                    ),
                )
            )
    # body = {"spec": {"template": {"spec": {"containers": [{"name": name, "resources": {"requests": {"cpu": cpu}}}]}}}}
    logger.info(f"{body}")

    # 使其成为子资源, 可以做到cr级联删除的效果
    kopf.adopt(body)

    try:
        apps_api.replace_namespaced_deployment(
            name=name,
            namespace=namespace,
            body=body,
        )
        logger.info(f"deployment is update: {name}")
    except Exception as e:
        status = getattr(e, "status")
        if status == 400:
            print(e)
            print("格式错误")
        elif status == 403:
            print("没权限")

