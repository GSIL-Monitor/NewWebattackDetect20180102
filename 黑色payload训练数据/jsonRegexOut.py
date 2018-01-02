# -*- coding: utf-8 -*-
import os,sys,re


global s
global t



s = '{"request":{"Auth":{"AppKey":"obk_creditease","Ticket":"58dc6f4ac10605135680067c1"},"JourneyNo":"","OrderID":"","EID":"110037192","UID":"","DateFrom":"2017-03-30","DateTo":"2017-03-31","SearchType":"1","Version":""}}'
t = '{"abList":[{"abValue":"A","abVersion":"170727_crm_jztj"}],"appVersion":"709.003","basic_params":"{\"app\":\"ctrip\",\"big_channel\":\"bus\",\"small_channel\":\"\",\"operat_system\":\"android\",\"big_client_type\":\"rn\",\"small_client_type\":\"\",\"client_version\":\"1.0.2\"}","bookable":1,"busNumber":"H0013","fromCity":"益阳","fromDate":"2017-12-29","fromStation":"赫山汽东站","fromTime":"13:30","fullPrice":35,"head":{"auth":"","cid":"32001168610068341825","ctok":"b691cbbf75384","cver":"709.003","lang":"01","sauth":"","sid":"8061","syscode":"32"},"isNeedBusInfo":true,"isNeedServPackInfo":false,"symbol":"3rUe_KYqWPUBOLGaswqnkyLD","toCity":"长沙星沙","toStation":"长沙星沙","utmsource":""}'
def regex(mubiao):
    global s
    global t
	
    patstr = '"[\w|\d]*\\\\{0,1}":'
    patobj = re.compile(patstr)
    result = patobj.findall(mubiao)
    if result:
       # result[0] = re.sub(pa)
        #regex(result[0])
       for rs in result:
           #print rs
           mubiao = mubiao.replace(rs,' ')
        #print result
    else:
        print('456')
    return mubiao


def regex2(mubiao):
    p = re.compile('(",|},|{|}|\,|\\\\)')
    mubiao = p.sub('',mubiao)
    p = re.compile('"')
    mubiao = p.sub('',mubiao)
    #mubiao = mubiao.replace('"', '')
    #mubiao = mubiao.replace('{', '')
    #mubiao = mubiao.replace('"}', '')
   # mubiao = mubiao.replace('}', '')
   # mubiao = mubiao.replace('},', '')
    return mubiao


if __name__ == '__main__':
    jsonOut = open('jsonFilter.txt', 'w',encoding='UTF-8')

    trainWhiteData = open('white_2.txt', 'r',encoding='UTF-8')
    lines = trainWhiteData.readlines()
    for line in lines:
        if line.startswith('{'):
            line = regex(line)
            line = regex2(line)
            jsonOut.writelines(line)
        else:
            jsonOut.writelines(line)



'''
if s.startswith('{'):

    s = regex(s)
    s = regex2(s)
    print(s)
    jsonOut.writelines(s+'\n')

if t.startswith('{'):
    t = regex(t)
    t = regex2(t)
    print(repr(t)) #.encode(encoding='UTF-8',errors='strict')
    jsonOut.writelines(t+'\n')
'''