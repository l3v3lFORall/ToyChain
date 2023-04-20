import fire
import datetime
import os
import utils.plugin as pluginAPI
import utils.common as commonAPI
from loguru import logger


class one():
    """
    one 加载各功能的主类
    """
    BANNER = '''
            ToyChain Playgound
            '''
    WORK_ROOT = os.path.abspath(os.path.dirname(__file__))
    def __init__(self, slience='n', target="baidu.com"):
        self.slience = slience
        self.target = target
        
    def printBanner(self):
        """
        printBanner 输出banner
        
                # slience (str, optional): 是否关闭banner输出. Defaults to 'n'.
        """
        if self.slience != "y":
            print(self.BANNER)
        print(datetime.datetime.now())
        
    def loadConfig(self, cfgPath="configs"):
        """
        loadConfig 加载configs中的所有配置文件

        Args:
            cfg_path (str, optional): 配置文件路径. Defaults to "configs".

        Returns:
            _type_: 配置字典，key是配置文件名
        """
        import yaml
        cfgFileNameList = os.listdir(cfgPath)
        cfgDict = {}
        for _cnl in cfgFileNameList:
            _file_path = os.path.join(cfgPath, _cnl)
            _name = _cnl.split('.')[0]
            cfgDict[_name] = yaml.safe_load(
                open(_file_path, "r", encoding="utf-8").read()
            )
            commonAPI.pDebug(f"| 加载配置文件：{_cnl}")
        runtimeCfg = cfgDict["runtimeCfg"]
        versionCfg = cfgDict["versionCfg"]
        return runtimeCfg, versionCfg, cfgDict
    def checkEnvir(self):
        def checkOS():
            """
            checkOS 运行平台检查

            Returns:
                str: "Windows" or "Linux"
            """
            import platform
            osp = platform.system()
            commonAPI.pDebug(f"| 当前运行平台: {osp}")
            return osp
        def checkNetwork(proxy):
            import requests
            import random
            times = 0
            commonAPI.pDebug(f'| 使用代理{proxy}检查网络连通性')
            while True:
                times += 1
                urls = ['https://www.baidu.com', 'https://www.google.com']
                url = random.choice(urls)
                timeout = 10
                try:
                    rsp = requests.get(url, proxies=proxy,
                                    timeout=timeout)
                except Exception as e:
                    commonAPI.pDebug(f'| Unable to access Internet, retrying for the {times}th time')
                else:
                    if rsp.status_code == 200:
                        return True
                if times >= 3:
                    commonAPI.pDebug(f'| 网络请求失败 {times}th')
                    return False
        
        self.envirOS = checkOS()
        return checkNetwork(self.runtimeCfg["proxy"])
    
    def cookRoutine(self):
        """
        cookRoutine : 按照runtimeCfg.yaml创建插件运行顺序、建立数据库
        """
        self.dbConn = commonAPI.openSqlite(f"out/{self.target}.db")
        return self.runtimeCfg["plugin"]
        
    @logger.catch()    
    def run(self):
        """
        run 运行工具
        """
        self.printBanner()
        self.runtimeCfg, self.versionCfg, self._Cfg = self.loadConfig()
        if self.checkEnvir() != True:
            print("| Check the Internet Connect!")
            return 1
        pluginRoutine = self.cookRoutine()
        commonAPI.pDebug(f'| 加载配置流程 {pluginRoutine}')
        for phase, plugin in pluginRoutine.items():
            commonAPI.pInfo(f"|- {phase}阶段 执行{plugin}")
            data = pluginAPI.startPlugin(
                phase, plugin, self.runtimeCfg, target=self.target
            )
            commonAPI.pDebug(f'| 得到数据 {data}')
if "__main__" in __name__:

    fire.Fire(one)