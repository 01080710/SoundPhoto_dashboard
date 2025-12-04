def parse_city(areaname: str):
    if '市' in areaname and (('區' not in areaname) or (areaname.index('區') > areaname.index('市'))):
        return areaname[:areaname.index('市')+1]
    elif '縣' in areaname:
        return areaname[:areaname.index('縣')+1]
    else:
        return '台中市'


def parse_town(areaname: str):
    # 區
    if '區' in areaname:
        si = areaname.index('市') if '市' in areaname else -1
        ui = areaname.index('區')
        if ui - si > 0:
            return areaname[si+1:ui+1]   # 包含 "區"
        else:
            return '其他'

    # 鄉
    if '鄉' in areaname:
        xi = areaname.index('縣') if '縣' in areaname else -1
        yi = areaname.index('鄉')
        if yi - xi > 0:
            return areaname[xi+1:yi+1]
        else:
            return '其他'

    # 鎮
    if '鎮' in areaname:
        xi = areaname.index('縣') if '縣' in areaname else -1
        yi = areaname.index('鎮')
        if yi - xi > 0:
            return areaname[xi+1:yi+1]
        else:
            return '其他'

    return '其他'


def parse_street(areaname: str):
    # 只處理 有「區」的情況，否則 "其他"
    if '區' not in areaname:
        return '其他'

    # 從區之後開始找
    start = areaname.index('區') + 1
    tail = areaname[start:]

    for kw in ['路', '街', '巷']:
        if kw in tail:
            end = tail.index(kw)
            return tail[:end] + kw

    return '其他'

