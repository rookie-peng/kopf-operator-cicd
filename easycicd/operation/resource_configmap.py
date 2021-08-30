import yaml
from configobj import ConfigObj


# def app_config(config):
def app_config():
    """
    处理代码仓库里面的configmap文件，生成应用配置
    :return: key: value
    """
    app_setting = []
    cfg = ConfigObj("./env.config", encoding='UTF-8')

    for k, v in cfg['app-setting'].items():
        app_setting.append({"name": k, "value": v})
    print(app_setting)

app_config()