import os
import utils.common as commonAPI
import utils.db as dbAPI
#https://www.cnblogs.com/Cl0ud/p/16065198.html

class Plugin():
    def __init__(self):
        self.pluginResult = None
        pass
    def run(self):
        pass
    def outtoFile(self):
        pass
    
    
def loadPlugin(_name):
    """
    loadPlugin 按名称加载指定插件

    Args:
        _name (str): 插件名称.
    """

    _fp = os.path.join("plugins", _name)
    customPlugin = __import__(_fp.replace(os.sep, '.'))
    customPlugin = eval(f"customPlugin.{_name}")
    return customPlugin

def resultAdd(da, db):
    """
    resultAdd 合并两个字典，相同键值则合并

    Args:
        da (dict): _description_
        db (dict): _description_

    Returns:
        _type_: _description_
    """
    # pDebug(str(da.keys()) + str(str(db.keys())))
    flag = {}
    for key in da.keys():
        if db.__contains__(key):
            flag[key] = da[key] + db.pop(key)
        else:
            flag[key] = da[key]
    flag.update(db)
    return flag 

def startPlugin(keyword, pDict, Config, target, other):
    """
    startPlugin 对目标target执行由keyword指定的某类型的所有插件

    Args:
        keyword (str): 流程所处阶段的名称
        pDict (list): 插件配置字典
        Config (dict): runtime中某阶段的配置
        target (str): 总目标
        other (dict): 上一个插件运行的中间结果

    Returns:
        _type_: 整理好的插件运行结果，格式如插件模板所示
    """
    if pDict == None:
        return None
    routine = {}
    for pName, pConfig in pDict.items():
        routine[keyword + '_' + pName] = pConfig
        
    pluginReturned = {}
    for pName, pConfig in routine.items():
        loadedPlugin = loadPlugin(pName)
        _Config = Config["plugin"][keyword][pName.split('_')[-1]]
        _Config["Target"] = target
        _Config["proxy"] = Config["proxy"]
        commonAPI.pDebug(f'| 即将运行插件 {pName}，使用配置：{_Config}')
        commonAPI.pDebug(other)
        temp = loadedPlugin.customPlugin().run(config=_Config, other=other)
        pluginReturned = resultAdd(pluginReturned, temp)
        other = pluginReturned
        target = pluginReturned["Target"]
        commonAPI.pDebug(f'| 得到数据 {pluginReturned}')
        dbAPI.save(Config["tempData"]["path"], pluginReturned)
        
    return pluginReturned
    
    
    
