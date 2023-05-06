
import utils.plugin as _up
from utils.common import pInfo


class customPlugin(_up.Plugin):
    """infoGather OneForAll 插件"""
    def __init__(self):
        self.TYPE = "infoGather"
        self.Target = []
        self.Result = {}
        self.Save = {
            "OutputPath":[],
            "Command":[],
            "CommandResult":[]
            }
        self.pluginResult = {
            "target": [],
            "result": {},
            "save": {}
        }
    
    def extractData(self, path):
        """提取一些工具输出的j文件中的通用信息

        Returns:
            _type_: _description_
        """
        # 依次处理所有的csv文件
        def _extract(_path):
            # pInfo(_path)
            _ = []
            # _path = r"C:\Users\33119\Desktop\ToyChain\module\OneForAll\results\baidu.com.csv"
            flag = False
            import csv
            with open(_path, "r", encoding="utf8", newline='') as _c:
                resultCsv = csv.reader(_c)
                for row in resultCsv:
                    if row[5] == "subdomain":
                        flag = True
                    else:
                        _.append(row[5])
            if flag != True:
                raise Exception("插件生成的表格不符合预期")
            return _
        import os
        result = []
        self.Result["subdomain"] = []
        # path = r"C:\Users\33119\Desktop\ToyChain\module\OneForAll\results"
        for _fn in os.listdir(path):
            if _fn.endswith(".csv"):
                result += _extract(os.path.join(path, _fn))
        # pInfo(result)
        # input()
        self.Result["subdomain"] = result
        self.pluginResult["result"] = self.Result

    
    def setEnv(self, kwargs):
        """
        设置插件使用代理/设定运行结果保存位置/拼接命令
        """
        pInfo(self.__doc__)
        import time
        outPath = f"out/infoGather_OneForAll/{int(round(time.time() * 1000))}"
        self.Save["OutputPath"].append(outPath)
        pInfo(f"|--设定结果导出位置：{outPath}")
        myProxy = "https://" + kwargs["config"]["proxy"]["https"]
        pInfo(f"|--正在使用代理：{myProxy}")
        cmd = kwargs["config"]["cmd"]
        import os 
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        targetPath = os.path.join(outPath, "targets.txt")
        self.Save["TargetPath"] = list(targetPath)

        with open(targetPath, "wb") as _f:
            _f.write(b'\n'.join([_.encode() for _ in kwargs["config"]["Target"]]))
    
        cmd = cmd.format(targetPath, outPath)
        pInfo(f"|--设定执行命令：{cmd}")
        self.Save["Command"].append(cmd)
        return outPath, myProxy, cmd
        
    def getResult(self, cmd):
        import subprocess
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error_msgs = res.communicate()
        import base64
        self.Save["CommandResult"].append(base64.b64encode(output).decode("utf8"))
        print(output.decode(encoding='utf-8'))

    def resultFilter(self, kwargs):
        """
        安装相邻执行的两个插件的需要对target进行修改
        """
        assert(type(kwargs["config"]["Target"]) == type([]))
        self.pluginResult["target"] = self.Result["subdomain"] + kwargs["config"]["Target"]
        self.pluginResult["target"] = list(set(self.pluginResult["target"]))
        self.pluginResult["result"] = self.Result
        self.pluginResult["save"] = self.Save
        return self.pluginResult


    def run(self, *args, **kwargs):
        """
        run 运行插件，Based on oneforall

        Args:
            kwargs["config"]: 导入的配置
            kwargs["other"]: 上一个插件运行的结果
            kwargs["config"]["Target"]应是包含待寻找子域名的url列表！！
        
        Returns:
            dict: {
                target(list):下一个插件的待测目标,
                result(dict):当前此插件的经过处理的运行结果,
                save(dict):此插件运行过程中的信息存档
            }
        """
        outPath, myProxy, cmd = self.setEnv(kwargs)
        self.getResult(cmd)
        self.extractData(outPath)
        self.pluginResult = self.resultFilter(kwargs)
        pInfo(f"输出子域名数量：{len(self.pluginResult['Target'])}")
        return self.pluginResult