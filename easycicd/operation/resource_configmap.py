import os
import yaml
import logging
from configobj import ConfigObj


# def app_config(config):
def app_config(root_path):
    """
    处理代码仓库里面的env.config文件，生成应用配置
    :return: list
    """
    app_setting = []
    cfg = ConfigObj(f"../../{root_path}/env.config", encoding='UTF-8')
    print('^^^^^^^^^^^^', root_path)
    try:
        for k, v in cfg['app-setting'].items():
            app_setting.append({"name": k, "value": v})
    except Exception as e:
        print(str(e))
    # print(app_setting)
    return app_setting


# app_config('zhipeng.su/sql-archery')