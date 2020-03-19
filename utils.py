def format_bytes(bytes):
    """
    把字节单位的格式化为适宜单位的
    :param str: 字节单位 字符串
    :return: 适宜单位的下载速度
    """
    byte_int=int(bytes)

    if byte_int < 0x400:
        return '{:d} B'.format(byte_int)
    byte_int /= 0x400
    for prefix in ('KB', 'MB', 'GB','TB', 'PB', 'EB', 'ZB'):
        if byte_int < 0x400:
            return '{:0.02f} {}'.format(byte_int, prefix)
        byte_int /= 0x400

def format_rate(completed,total):
    """
    获取下载进度百分比
    :param completed:  已经下载大小
    :param total: 下载文件总大小
    :return: 字符串 下载进度百分比
    """
    completeds= int(completed)
    totals=int(total)
    if totals ==0:
        return "0.00%"
    else:
        return "%.2f%%"%(completeds/totals*100)



