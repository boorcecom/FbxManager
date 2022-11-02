#!/usr/bin/python3

import os
import sys
import base64
import importlib.util
import time
fbxmlib = importlib.util.spec_from_file_location("fbxm_lib", os.getenv('HOME')+"/fbxmanager/fbxm_lib.py")
fbxm_lib = importlib.util.module_from_spec(fbxmlib)
fbxmlib.loader.exec_module(fbxm_lib)

vmname=sys.argv[1]


vms=fbxm_lib.doApiGet("/vm/")
if vms['success']:
    for vm in vms['result']:
        if vm['name']==vmname:
            id=str(vm['id'])
            if vm['status']=="starting":
                time.sleep(30)
                vm=fbxm_lib.doApiGet("/vm/"+id)['result']
                if vm['status']=="starting":
                    fbxm_lib.doApiPost("/vm/"+id+"/stop")
                    time.sleep(10)
                    vm=fbxm_lib.doApiGet("/vm/"+id)['result']
            if vm['status']=="running":
                #os.system("ssh -o StrictHostKeyChecking=no freebox@"+vmname+" sudo poweroff")
                fbxm_lib.doApiPost("/vm/"+id+"/powerbutton")
                count=0
                while count<30 and vm['status']!='stopped':
                    time.sleep(10)
                    vm=fbxm_lib.doApiGet("/vm/"+id)['result']
                    count=count+1
            if vm['status']=="stopping":
                count=0
                while count<30 and vm['status']!='stopped':
                    time.sleep(10)
                    vm=fbxm_lib.doApiGet("/vm/"+id)['result']
                    count=count+1
                if vm['status']=="stopping":
                    fbxm_lib.doApiPost("/vm/"+id+"/stop")
                    time.sleep(10)
                    vm=fbxm_lib.doApiGet("/vm/"+id)['result']

