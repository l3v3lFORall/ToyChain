import utils.common as commonAPI



def save(path, data):
    try:
        import time, os
        tempDataName = str(int(round(time.time() * 1000))) + '.json'
        tempDataPath = os.path.join(path, tempDataName)
        import json
        with open(tempDataPath, "w") as _f:
            json.dump(data, _f)
        commonAPI.pDebug(f"|-临时输出写入{tempDataPath}")
    except Exception as e:
        commonAPI.pInfo(f"|-临时输出写入出错 {e}")