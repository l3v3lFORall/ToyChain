
import utils.plugin as _up
from utils.common import pInfo


class customPlugin(_up.Plugin):
    """
    infoGather ksubdomain是一款基于无状态的子域名爆破工具，
    类似无状态端口扫描，支持在Windows/Linux/Mac上进行快速的DNS爆破，
    拥有重发机制不用担心漏包。
    https://github.com/boy-hack/ksubdomain
    """
    def __init__(self):
        self.TYPE = "infoGather"
        self.pluginResult = {
            "subdomain": [],
            "ip": [],
            "other": [],
            "Target": []
        }
        
    def extractData(self, path):
        """提取一些工具输出的j文件中的通用信息

        Returns:
            _type_: _description_
        """
        result = []
        with open(path, "r") as _f:
            for _line in _f.readlines():
                _line = _line.split("=>")[0]
                result.append(_line)
        self.pluginResult["subdomain"] = result
        return self.pluginResult

    
    def setEnv(self, kwargs):
        """
        设置插件使用代理/设定运行结果保存位置/拼接命令
        """
        # pInfo(self.__doc__)
        import time
        outPath = f"out/infoGather_ksubdomain/{int(round(time.time() * 1000))}"
        resultPath = outPath + "/ksubdomain.txt"
        pInfo(f"|--设定结果导出位置：{outPath}")
        myProxy = "https://" + kwargs["config"]["proxy"]["https"]
        pInfo(f"|--正在使用代理：{myProxy}")
        cmd = kwargs["config"]["cmd"]
        import os 
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        targetPath = os.path.join(outPath, "targets.txt")
        if type(kwargs["config"]["Target"]) == type(""):
            temp = [kwargs["config"]["Target"]]
        with open(targetPath, "wb") as _f:
            _f.write(b'\n'.join([_.encode() for _ in temp]))
    
        cmd = cmd.format(targetPath, resultPath)
        pInfo(f"|--设定执行命令：{cmd}")
        return outPath, myProxy, cmd, resultPath
        
    def getResult(self, cmd):
        import subprocess
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error_msgs = res.communicate()
        print(output.decode(encoding='utf-8'))

    def resultFilter(self, kwargs):
        """
        安装相邻执行的两个插件的需要对target进行修改
        """
        pInfo(f"")
        self.pluginResult["Target"] = self.pluginResult["subdomain"] + [kwargs["config"]["Target"]]
        self.pluginResult["Target"] = list(set(self.pluginResult["Target"]))
        return self.pluginResult


    def run(self, *args, **kwargs):
        """
        run 运行插件，Based on https://xxx

        Args:
            kwargs["config"]: 导入的配置
        
        Returns:
            dict: 提取子域名、APP数据，保存导出文件的路径
        """
        outPath, myProxy, cmd, resultPath = self.setEnv(kwargs)
        self.getResult(cmd)
        self.pluginResult = self.extractData(resultPath)
        self.pluginResult["other"].append(outPath)
        self.pluginResult = self.resultFilter(kwargs)
        pInfo(f"输出子域名数量：{len(self.pluginResult['Target'])}")
        # print(self.pluginResult['Target'])
        return self.pluginResult
    

if __name__ == "__main__":
    a = customPlugin()
    # a.run(
    #     config={"proxy":{"https":"127.0.0.1:56789"},"Target":["kiwi.com"],"cmd":"module/ksubdomain/ksubdomain enum --dl {} -o {} --skip-wild"}
    # )