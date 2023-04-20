
import utils.plugin as _up
from utils.common import pInfo


class customPlugin(_up.Plugin):
    """infoGather 工具ENScanGO plugin"""
    def __init__(self):
        self.TYPE = "infoGather"
        self.pluginResult = {
            "subdomain": [],
            "ip": [],
            "other": []
        }
        
    def extractData(self):
        data = {}
        return data
    def run(self, *args, **kwargs):
        """
        run 运行插件，Based on https://github.com/wgpsec/ENScan_GO

        Args:
            kwargs["config"]: 导入的配置
        
        Returns:
            _type_: _description_
        """
        outPath = "out/infoGather_ENScan/"
        myProxy = "https://" + kwargs["config"]["proxy"]["https"]
        cmd = kwargs["config"]["cmd"]
        # cmd: "ENScanGO.exe -is-merge -branch -o {} -n {}"
        pInfo(self.__doc__)
        pInfo(f"|--正在使用代理：{myProxy}")
        pInfo(f"|--设定结果导出位置：{outPath}")
        import os 
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        cmd = cmd.format(outPath, kwargs["config"]["Target"])
        pInfo(f"|--设定执行命令：{cmd}")
        import subprocess
        
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error_msgs = res.communicate()
        print(output.decode(encoding='utf-8'))
        
        self.pluginResult["other"].append(outPath)
        return self.pluginResult