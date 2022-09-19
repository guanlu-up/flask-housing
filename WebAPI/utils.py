import re
from subprocess import Popen, PIPE


def local_ipaddress(net="en0"):
    """返回本机指定网卡的IPV4地址"""
    command = f"ifconfig {net}"
    terminal = Popen(command, shell=True, stdout=PIPE)
    stdout, stderr = terminal.communicate()
    if not stdout:
        return None
    netinfo = stdout.decode("utf-8")
    search = re.search('.*inet(.*?)netmask', netinfo)
    if search is None or not search.lastindex:
        return None
    return search.group(1).strip()
