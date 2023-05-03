
import utils.plugin as _up
from utils.common import pInfo


class customPlugin(_up.Plugin):
    """
    infoGather 插件样例
    """
    def __init__(self):
        self.TYPE = "infoGather"
        self.pluginResult = {
            "subdomain": [],
            "ip": [],
            "other": []
        }
        
    def extractData(self, path):
        """提取一些工具输出的j文件中的通用信息

        Returns:
            _type_: _description_
        """
        return self.pluginResult

    
    def setEnv(self, kwargs):
        """
        设置插件使用代理/设定运行结果保存位置/拼接命令
        """
        pInfo(self.__doc__)
        import time
        outPath = f"out/infoGather_ENScan/{int(round(time.time() * 1000))}"
        pInfo(f"|--设定结果导出位置：{outPath}")
        myProxy = "https://" + kwargs["config"]["proxy"]["https"]
        pInfo(f"|--正在使用代理：{myProxy}")
        cmd = kwargs["config"]["cmd"]
        import os 
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        cmd = cmd.format(outPath, kwargs["config"]["Target"])
        pInfo(f"|--设定执行命令：{cmd}")
        return outPath, myProxy, cmd
        
    def getResult(self, cmd):
        import subprocess
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error_msgs = res.communicate()
        print(output.decode(encoding='utf-8'))

    def resultFilter(self):
        """
        安装相邻执行的两个插件的需要对target进行修改
        """
        self.pluginResult["Target"] = self.pluginResult["Target"]
        return self.pluginResult


    def run(self, *args, **kwargs):
        """
        run 运行插件，Based on https://xxx

        Args:
            kwargs["config"]: 导入的配置
        
        Returns:
            dict: 提取子域名、APP数据，保存导出文件的路径
        """

        outPath, myProxy, cmd = self.setEnv(kwargs)
        self.getResult(cmd)
        self.pluginResult = self.extractData(outPath)
        self.pluginResult["other"].append(outPath)
        self.pluginResult = self.resultFilter()

        return self.pluginResult