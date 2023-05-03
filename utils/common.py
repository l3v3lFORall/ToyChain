from loguru import logger
import sys
import sqlite3


LOG_PATH = "out/runtime.log"
# 日志配置
# 终端日志输出格式
stdout_fmt = '<cyan>{time:HH:mm:ss,SSS}</cyan> ' \
             '[<level>{level: <5}</level>] ' \
             '<blue>{module}</blue>:<cyan>{line}</cyan> - ' \
             '<level>{message}</level>'
# 日志文件记录格式
logfile_fmt = '<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green> ' \
              '[<level>{level: <5}</level>] ' \
              '<cyan>{process.name}({process.id})</cyan>:' \
              '<cyan>{thread.name: <18}({thread.id: <5})</cyan> | ' \
              '<blue>{module}</blue>.<blue>{function}</blue>:' \
              '<blue>{line}</blue> - <level>{message}</level>'
def setL(path=LOG_PATH):
    _l = logger.add(path, rotation="5 MB")
    return _l

def pInfo(data):
    logger.info(data)
    
def pDebug(data):
    logger.debug(data)

def pError(data):
    logger.error(data)
    
logger.remove()
logger.level(name='TRACE', color='<cyan><bold>')
logger.level(name='DEBUG', color='<blue><bold>')
logger.level(name='INFOR', no=20, color='<green><bold>')
logger.level(name='QUITE', no=25, color='<green><bold>')
logger.level(name='ALERT', no=30, color='<yellow><bold>')
logger.level(name='ERROR', color='<red><bold>')
logger.level(name='FATAL', no=50, color='<RED><bold>')
# 命令终端日志级别默认为INFOR
logger.add(sys.stderr, level='INFOR', format=stdout_fmt, enqueue=True)
# 日志文件默认为级别为DEBUG
logger.add(LOG_PATH, level='DEBUG', format=logfile_fmt, enqueue=True, encoding='utf-8')

####################################################################

@logger.catch
def checkVersion(url, version):
    """
    checkVersion 检查是否需要更新，但当前私人项目暂不能使用

    Args:
        url (_type_): _description_
        version (_type_): _description_
    """
    pDebug("| 正在检查更新")
    import requests
    version_url = url.replace("github.com", "raw.githubusercontent.com") + "/main/configs/versionCfg.yaml"
    remote_version = requests.get(version_url).json()["version"]
    if remote_version != version:
        pInfo("| 最近有更新")
        return True
    return False


# def outputXLSX(data, path="out/default.xlsx"):
#     """
#     outputXLSX 数据导出

#     Args:
#         data (_type_): _description_
#         path (str, optional): _description_. Defaults to "out/default.xlsx".
#     """
#     # TODO 等有一个初步数据之后，完成这部分
#     # https://openpyxl-chinese-docs.readthedocs.io/zh_CN/latest/tutorial.html
#     pInfo("正在导出到文件")
#     # import openpyxl
#     # opwb = openpyxl.Workbook()
#     # ws = opwb.create_sheet("test")
    
#     # x,y = 1,1
#     # ws.cell(row=x, colum=y, value=data[x][y])
#     # opwb.save(path)