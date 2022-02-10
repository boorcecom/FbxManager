#!/usr/bin/python3

import sys
import os
import time
import base64
import importlib.util
fbxmlib = importlib.util.spec_from_file_location("fbxm_lib", os.getenv('HOME')+"/fbxmanager/fbxm_lib.py")
fbxm_lib = importlib.util.module_from_spec(fbxmlib)
fbxmlib.loader.exec_module(fbxm_lib)

vmname=sys.argv[1]

fileQCOW2="/Freebox/VMs/"+vmname+".qcow2"
fileEFIVARS="/Freebox/VMs/"+vmname+".qcow2.efivars"
destination="/EXTERNAL/VM"

vms=fbxm_lib.doApiGet("/vm/")
if vms['success']:
    for vm in vms['result']:
        if vm['name']==vmname:
            vm_old_stat=vm['status']

os.system("sudo -u freebox /home/freebox/fbxmanager/stopVM.py "+vmname)

request={"files": [ base64.b64encode(fileQCOW2.encode()).decode() , base64.b64encode(fileEFIVARS.encode()).decode(), ], "dst": base64.b64encode(destination.encode()).decode() , "mode" :"overwrite" }
copy_request=fbxm_lib.doApiPostJSON("/fs/cp/",request)

if not(copy_request['success']):
    sys.exit("Copy request failure")

task_id=str(copy_request['result']['id'])

task_status=fbxm_lib.doApiGet('/fs/tasks/'+task_id)['result']['state']

while task_status!='done' and task_status!='failed':
    time.sleep(30)
    task_status=fbxm_lib.doApiGet('/fs/tasks/'+task_id)['result']['state']

if vm_old_stat=='running':
    os.system("sudo -u freebox /home/freebox/fbxmanager/startVM.py "+vmname)


if task_status=='failed':
    sys.exit('copy failed')

fbxm_lib.doApiDelete('/fs/tasks/'+task_id)

