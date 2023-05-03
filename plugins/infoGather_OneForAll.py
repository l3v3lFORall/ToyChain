
import utils.plugin as _up
from utils.common import pInfo


class customPlugin(_up.Plugin):
    """infoGather OneForAll 插件"""
    def __init__(self):
        self.TYPE = "infoGather"
        self.pluginResult = {
            "subdomain": ["baidu.com", "https://img.baidu.com"],
            "ip": ["127.0.0.1", "10.0.0.1/24"],
            "other": ["a.txt", "b.xlsx"]
        }
    def extractData(self, path):
        pass




    def run(self, *args, **kwargs):
        """
        run 运行插件，Based on oneforall

        Args:
            kwargs["config"]: 导入的配置
            kwargs["other"]: 上一个插件运行的结果
        
        Returns:
            dict: 提取子域名、APP数据，保存导出文件的路径
        """
        import time
        outPath = f"out/infoGather_OneForAll/{int(round(time.time() * 1000))}"
        myProxy = "https://" + kwargs["config"]["proxy"]["https"]
        cmd = kwargs["config"]["cmd"]
        pInfo(self.__doc__)
        pInfo(f"|--正在使用代理：{myProxy}")
        pInfo(f"|--设定结果导出位置：{outPath}")
        import os 
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        targetPath = os.path.join(outPath, "targets.txt")
        with open(targetPath, "wb") as _f:
            _f.write(b'\n'.join([_.encode() for _ in [kwargs["config"]["Target"]]]))
    
        cmd = cmd.format(targetPath, outPath)
        pInfo(f"|--设定执行命令：{cmd}")

        import subprocess
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error_msgs = res.communicate()
        print(output.decode(encoding='utf-8'))
        # do something

        try:
            self.extractData(outPath)
        except Exception as e:
            pInfo(f"|--插件提取数据出错：{e}")

        return self.pluginResult