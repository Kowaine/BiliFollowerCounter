"""
@Author: Kowaine
@Description: 更新
@Date: 2021-02-06 01:32:14
@LastEditTime: 2021-02-06 12:10:52
"""

import time

def get_formatted_time(any_time=time.time()):
    """
    获取格式化的时间字符串 \n
    @args: \n
        any_time 任意合法时间戳
    @returns: \n 
        格式化后的时间字符串 :string
    """
    formatter = "{}_{:0>2d}{:0>2d}_{:0>2d}{:0>2d}{:0>2d}"
    temp_time = time.localtime(any_time)
    formatted_time = formatter.format(temp_time.tm_year, temp_time.tm_mon, temp_time.tm_mday, temp_time.tm_hour, temp_time.tm_min, temp_time.tm_sec)
    return formatted_time


import configparser, os
# 默认的配置文件
CONFIG_FILE = "config.ini"

class Configer():
    """
    配置文件管理类 \n
    """

    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """
        读取配置文件并返回嵌套字典 \n
        """
        cfg = configparser.ConfigParser()
        # print(os.path.join(self.config_file))
        cfg.read(os.path.join(self.config_file), encoding="utf-8")

        conf = {}

        # 遍历section
        for section in cfg.sections():
            # 遍历键值对并重组为字典
            temp_dict = {}
            for item in cfg.items(section):
                temp_dict[item[0]] = item[1]
            conf[section] = temp_dict

        # print(conf)

        self.conf = conf
    
    def reload_config(self, config_file=None):
        """
        重新加载配置文件(可能用不上) \n
        """
        if config_file:
            self.config_file = config_file
        self.load_config()

    def get_ups(self):
        """
        获取up主uid列表 \n
        @returns: \n
            配置中up主uid列表 :tuple
        """
        try:
            return self.conf['ups']['uid'].split(",")
        except Exception:
            return []

def run():
    import subprocess
    import requests
    import json
    import os

    # 粉丝数量api
    API = "https://api.bilibili.com/x/relation/stat?vmid={uid}&jsonp=jsonp"

    cfg = Configer()
    ups = cfg.get_ups()

    if  os.path.exists("data") and os.path.isdir("data"):
        pass
    else:
        os.makedirs("data")
    
    for up in ups:
        url = API.format(uid=up)
        response = requests.get(url)
        response.encoding = "utf-8"
        data = json.loads(response.text)
        
        # 创建文件或追加内容
        filename = os.path.join("data", "".join([up, ".txt"]))
        content = "".join([get_formatted_time(), " ", str(data['data']['follower']), "\n"])
        if os.path.exists(filename):
            with open(filename, "a", encoding="utf-8") as f:
                f.write(content)
        else:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == '__main__':
    run()
