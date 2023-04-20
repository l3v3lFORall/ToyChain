
import utils.plugin as _up



class customPlugin(_up.Plugin):
    """infoGather p_lugin 模板测试"""
    def __init__(self):
        self.TYPE = "infoGather"
        self.pluginResult = {
            "subdomain": ["baidu.com", "https://img.baidu.com"],
            "ip": ["127.0.0.1", "10.0.0.1/24"],
            "other": ["a.txt", "b.xlsx"]
        }
    def run(self, *args, **kwargs):
        print(kwargs["target"])
        # do something
        return self.pluginResult