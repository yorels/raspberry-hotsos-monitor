from pyroute2 import iwutil
from pyroute2.iproute import IPRoute
from pyroute2.netlink import NetlinkError


def is_wireless_interface(interface):
    ip = IPRoute()
    iw = iwutil.IW()
    index = ip.link_lookup(ifname=interface)[0]
    try:
        iw.get_interface_by_ifindex(index)
        print("wireless interface")
    except NetlinkError as e:
        if e.code == 19:  # 19 'No such device'
            print("not a wireless interface")
    finally:
        iw.close()
        ip.close()
