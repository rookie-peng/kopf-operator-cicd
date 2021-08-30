import os
import kopf
import yaml
from kubernetes import client
from easycicd.builder import python_builder


@kopf.on.create('EasyCicd')
def create_fn(spec, name, namespace, logger, **kwargs):
    repo = spec.get('gitrepo')
    gitbranch = spec.get('gitbranch')
    type = spec.get('type')
    replicas = spec.get('replicas')
    labels = {'app': name, 'superpeng': 'easycicd', 'branch': gitbranch}  # 不区分数据类型，都要加引号
    image = "busybox:latest"
    env = """
        - name: mysql
          value: '1.1.1.1:3306'
        - name: DEBUG
          value: 'False'
    """

    path = os.path.join(os.path.dirname(__file__), 'deploy.yaml')
    with open(path, 'rt') as f:
        tmpl = f.read()
    text = tmpl.format(name=name, namespace=namespace, replicas=replicas, env=env, image=image, app=labels['app'], branch=labels['branch'], superpeng=labels['superpeng'])
    body = yaml.safe_load(text)
    # 使其成为子资源, 可以做到cr级联删除的效果
    kopf.adopt(body)

    apps_api = client.AppsV1Api()

    # body = client.V1Deployment(
    #             api_version="apps/v1",
    #             kind="Deployment",
    #             metadata=client.V1ObjectMeta(name=name),
    #             spec=client.V1DeploymentSpec(
    #                 replicas=replicas,
    #                 selector={'matchLabels': labels},
    #                 template=client.V1PodTemplateSpec(
    #                     metadata=client.V1ObjectMeta(labels=labels),
    #                     spec=client.V1PodSpec(
    #                         containers=[client.V1Container(
    #                             name=name,
    #                             image=image
    #                         )]
    #                     )
    #                 ),
    #             )
    #         )

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
    env = """
        - name: mysql
          value: '1.1.1.1:3306'
        - name: DEBUG
          value: 'False'
    """

    path = os.path.join(os.path.dirname(__file__), 'deploy.yaml')
    with open(path, 'rt') as f:
        tmpl = f.read()
    text = tmpl.format(name=name, namespace=namespace, replicas=replicas, env=env, image=image, app=labels['app'], branch=labels['branch'], superpeng=labels['superpeng'])
    body = yaml.safe_load(text)
    # 使其成为子资源, 可以做到cr级联删除的效果
    kopf.adopt(body)

    apps_api = client.AppsV1Api()
    # body = client.V1Deployment(
    #             api_version="apps/v1",
    #             kind="Deployment",
    #             metadata=client.V1ObjectMeta(name=name),
    #             spec=client.V1DeploymentSpec(
    #                 replicas=replicas,
    #                 selector={'matchLabels': labels},
    #                 template=client.V1PodTemplateSpec(
    #                     metadata=client.V1ObjectMeta(labels=labels),
    #                     spec=client.V1PodSpec(
    #                         containers=[client.V1Container(
    #                             name=name,
    #                             image=image
    #                         )]
    #                     )
    #                 ),
    #             )
    #         )
    # body = {"spec": {"template": {"spec": {"containers": [{"name": name, "resources": {"requests": {"cpu": cpu}}}]}}}}

    try:
        apps_api.patch_namespaced_deployment(
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
    return {'deployment': name, 'author': 'superpeng'}
