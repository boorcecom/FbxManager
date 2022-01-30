#!/usr/bin/python3

import os
import sys
import base64
import importlib.util
fbxmlib = importlib.util.spec_from_file_location("fbxm_lib", "/home/freebox/fbxmanager/fbxm_lib.py")
fbxm_lib = importlib.util.module_from_spec(fbxmlib)
fbxmlib.loader.exec_module(fbxm_lib)

if fbxm_lib.doApiGet("/vm/2")["result"]["status"]!="running":
    if not(fbxm_lib.doApiPost("/vm/2/start")["success"]):
        sys.exit("Start darkstar02 failed")

os.system("ssh darkstar02 fbxmanager/backup.py")        


