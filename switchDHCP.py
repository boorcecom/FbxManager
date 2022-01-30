#!/usr/bin/python3

import sys
import importlib.util
fbxmlib = importlib.util.spec_from_file_location("fbxm_lib", "/home/freebox/fbxmanager/fbxm_lib.py")
fbxm_lib = importlib.util.module_from_spec(fbxmlib)
fbxmlib.loader.exec_module(fbxm_lib)

target=sys.argv[1]

if target=='start':
    payload={ "enabled": True, }
    fbxm_lib.doApiPutJSON('/dhcp/config/',payload)
    payload={ "use_custom_dns": False, }
    fbxm_lib.doApiPutJSON('/dhcpv6/config/',payload)
elif target=='stop':
    payload={ "enabled": False, }
    fbxm_lib.doApiPutJSON('/dhcp/config/',payload)
    payload={ "use_custom_dns": True, }
    fbxm_lib.doApiPutJSON('/dhcpv6/config/',payload)


