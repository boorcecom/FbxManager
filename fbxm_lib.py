#!/usr/bin/python3

import requests
import json
import time
import os.path
from hashlib import sha1
import hmac
import sys
import socket

FBXM_PATH=os.getenv('HOME')+"/fbxmanager"
FBXM_APTOK_FILE=FBXM_PATH+"/app.token"
FBXM_SESSTOK_FILE=FBXM_PATH+"/sess.token"
FreeBoxip="192.168.0.254"
apiPath="/api/"
apiVersion="8"
apiUrl="http://"+FreeBoxip+apiPath+"/v"+apiVersion+"/"
FBXM_version="0.0.3"
HostName=socket.gethostname()

def getAppToken():
    request = { "app_id": "com.boorce.fbxm","app_name": "FBXShell Manger","app_version": FBXM_version,"device_name": HostName }
    answer=requests.post(apiUrl+"login/authorize",json=request).json()
    if not(answer["success"]): 
        print("error : %s " % answer["msg"] )
        sys.exit("getAppTocken ended.")
    appToken=answer["result"]["app_token"]
    trackID=answer["result"]["track_id"]
    fDesc=open(FBXM_APTOK_FILE,"w")
    fDesc.write(appToken)
    fDesc.close()
    # Attente de la validation
    while True:
        answer=requests.get(apiUrl+"login/authorize/"+str(trackID)).json()
        if not(answer["success"]): 
            print("error : %s " % answer["msg"] )
            sys.exit("getAppToken ended.")
        print(answer)
        if answer["result"]["status"] == "granted":
            print("access granted !")
            break
        elif answer["result"]["status"] != "pending":
            sys.exit("timeout/denied sur grant !")
        time.sleep(5)

def createSession():
    getApiInfos=requests.get("http://"+FreeBoxip+"/api_version").json()
    apiPath=getApiInfos["api_base_url"]
    apiVersion=getApiInfos["api_version"][0]
    if not(os.path.exists(FBXM_APTOK_FILE)):
        getAppToken()
    # Récupération du challenge
    login=requests.get("http://"+FreeBoxip+apiPath+"/v"+apiVersion+"/login/").json()
    if not(login["success"]):
        print("createSession error : %s " % login["msg"])
        sys.exit("failed")    
    if login["result"]["logged_in"]:
        fDesc=open(FBXM_SESSTOK_FILE,"r")
        sessionToken=fDesc.readline()
        fDesk.close()
        return sessionToken
    challenge=login["result"]["challenge"]
    fDesc=open(FBXM_APTOK_FILE,"r")
    appToken=fDesc.readline().rstrip("\n")
    fDesc.close()
    password=hmac.new(appToken.encode(),challenge.encode(),"sha1").hexdigest()
    request={ 'app_id': 'com.boorce.fbxm', 'password': password }
    answer=requests.post("http://"+FreeBoxip+apiPath+"/v"+apiVersion+"/login/session/",data=json.dumps(request)).json()
    if not(answer["success"]):
        print("error : %s " % answer["msg"] )
        sys.exit("createSession ended.")        
    sessionToken=answer["result"]["session_token"]
    fDesc=open(FBXM_SESSTOK_FILE,"w")
    fDesc.write(sessionToken)
    fDesc.close()    
    return sessionToken

def doApiPost(apiName):
    sessionToken=createSession()
    answer=requests.post("http://"+FreeBoxip+apiPath+"/v"+apiVersion+apiName,headers={ "X-Fbx-App-Auth":sessionToken}).json()    
    return answer    

def doApiPostJSON(apiName,jsonRequest):
    sessionToken=createSession()
    answer=requests.post("http://"+FreeBoxip+apiPath+"/v"+apiVersion+apiName,json=jsonRequest, headers={ "X-Fbx-App-Auth":sessionToken}).json()    
    return answer    

def doApiGet(apiName):
    sessionToken=createSession()
    answer=requests.get("http://"+FreeBoxip+apiPath+"/v"+apiVersion+apiName,headers={ "X-Fbx-App-Auth":sessionToken}).json()
    return answer 

def doApiPut(apiName):
    sessionToken=createSession()
    answer=requests.put("http://"+FreeBoxip+apiPath+"/v"+apiVersion+apiName,headers={ "X-Fbx-App-Auth":sessionToken}).json()
    return answer

def doApiPutJSON(apiName,jsonRequest):
    sessionToken=createSession()
    answer=requests.put("http://"+FreeBoxip+apiPath+"/v"+apiVersion+apiName,json=jsonRequest, headers={ "X-Fbx-App-Auth":sessionToken}).json()
    return answer

def doApiDelete(apiName):
    sessionToken=createSession()
    answer=requests.delete("http://"+FreeBoxip+apiPath+"/v"+apiVersion+apiName,headers={ "X-Fbx-App-Auth":sessionToken}).json()
    return answer

def doApiDeleteJSON(apiName,jsonRequest):
    sessionToken=createSession()
    answer=requests.delete("http://"+FreeBoxip+apiPath+"/v"+apiVersion+apiName,json=jsonRequest, headers={ "X-Fbx-App-Auth":sessionToken}).json()
    return answer


