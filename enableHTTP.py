#!/usr/bin/python3

import os
import base64
import importlib.util
fbxmlib = importlib.util.spec_from_file_location("fbxm_lib", os.getenv('HOME')+"/fbxmanager/fbxm_lib.py")
fbxm_lib = importlib.util.module_from_spec(fbxmlib)
fbxmlib.loader.exec_module(fbxm_lib)


redirections=fbxm_lib.doApiGet("/fw/redir/")
if redirections['success']:
    for redirection in redirections["result"]:
        if not (redirection["enabled"]) and redirection["src_ip"]=='0.0.0.0' and redirection["lan_ip"]=='192.168.0.253' and redirection["ip_proto"]=='tcp' and (redirection["wan_port_start"]==80 or redirection["wan_port_start"]==443):
            id=str(redirection["id"])
            request={ "enabled": True }
            answer=fbxm_lib.doApiPutJSON("/fw/redir/"+id,request)

