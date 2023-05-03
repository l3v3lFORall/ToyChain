
import utils.plugin as _up
from utils.common import pInfo


class customPlugin(_up.Plugin):
    """
    infoGather 工具ENScanGO plugin
    一款基于各大企业信息API的工具，解决在遇到的各种针对国内企业信息收集难题。一键收集控股公司ICP备案、APP、小程序、微信公众号等信息聚合导出。
    https://github.com/wgpsec/ENScan_GO
    """
    def __init__(self):
        self.TYPE = "infoGather"
        self.pluginResult = {
            "subdomain": [],
            "ip": [],
            "other": []
        }
        
    def extractData(self, path):
        """提取一些工具输出的xlsx文件中的通用信息

        Returns:
            _type_: _description_
        """
        try:
            def extractICP():
                result = []
                ws = resultXlsx['ICP备案']
                if ws["C1"].value != "域名":
                    raise Exception("ICP备案的结果不符合预期")
                for row in ws[f'C2:C{ws.max_row}']:
                    for cell in row:
                        result.append(cell.value)
                return result
            def extractAPP():
                result = []
                ws = resultXlsx['APP']
                if ws["A1"].value != "名称":
                    raise Exception("APP信息的结果不符合预期")
                for row in ws[f'A2:A{ws.max_row}']:
                    for cell in row:
                        result.append(cell.value)
                return result            
            import os
            fileList = os.listdir(path)
            from openpyxl import load_workbook
            for _fl in fileList:
                resultXlsx = load_workbook(
                    os.path.join(path, _fl)
                )
                self.pluginResult["subdomain"] = extractICP()
                self.pluginResult["app"] = extractAPP()
                continue
        except Exception as e:
            pInfo(f"|--插件提取数据出错：{e}")

    
    
    def run(self, *args, **kwargs):
        """
        run 运行插件，Based on https://github.com/wgpsec/ENScan_GO

        Args:
            kwargs["config"]: 导入的配置
        
        Returns:
            dict: 提取子域名、APP数据，保存导出文件的路径
        """
        import time
        outPath = f"out/infoGather_ENScan/{int(round(time.time() * 1000))}"
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
        try:
            self.extractData(outPath)
            self.pluginResult["other"].append(outPath)
            pInfo(f"|--获取子域名{len(self.pluginResult['subdomain'])}条，APP信息{len(self.pluginResult['app'])}条；导出文件到{self.pluginResult['other']}")
            self.pluginResult["Target"] = kwargs["config"]["Target"]
        except Exception as e:
            pInfo(f"|--插件提取数据出错：{e}")
        return self.pluginResult