#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: vcy陈莹 <ying.chen@Ctrip.com>
# Date: 2017/12/26 17:02
from __future__ import unicode_literals
import datetime
import codecs
from tornado.escape import json_decode

from elasticsearch_dsl import Search, Q, A
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=['infosecuser:cRTw8GSCvu@sg.infosec.ctripcorp.com:80'])

def search(index_fmt, query_list, start_time, end_time):
    index_list = get_indexes_by_time(index_fmt, start_time, end_time)
    print index_list
    if isinstance(index_list, str):
        index_list = [index_list]

    rs = Search(index=index_list)
    s = rs.query().filter(query_list)
    s = s[0:10000]
    return s.execute()

def get_indexes_by_time(index_fmt, time_from, time_end):
    # time_from -= datetime.timedelta(hours=8)
    # time_end -= datetime.timedelta(hours=8)
    index_list = set()
    while time_from <= time_end:
        index_list.add(time_from.strftime(index_fmt))
        # 循环去得到所有index
        time_from += datetime.timedelta(days=1)
    index_list.add(time_end.strftime(index_fmt))
    return list(index_list)

if __name__ == '__main__':
    time_start = datetime.datetime(2018, 01, 01, 0, 01)   # 起始查询时间
    time_end = datetime.datetime.now()             # 结束查询时间， 默认是当前
    time_interval = 0.1  # 查询时间间隔, 单位小时
    time_range = 0.1     # 每次查询时间长度， 单位小时

    # ES 索引
    #index_fmt = "nile_ml-%Y.%m.%d"  # nile_ml
    index_fmt = "pprobe-%Y.%m.%d"   # pprobe

    # 查询条件
    # (nile_ml) 规则没中，中了机器学习  （误报）
    # q = Q("term", is_black=False) & Q("term", rule_result="white") & Q("term", is_ml=True)
    # (nile_ml) 中了黑名单和规则，但是没有中机器学习 （漏报）
    #q = (Q("term", is_black=True) | Q("term", rule_result="black")) & Q("term", is_ml=False) & Q("term", method="POST")
   # q = (Q("term", is_black=False) | Q("term", rule_result="white")) & Q("term", method="POST")

    # (pprobe) 只查post数据
    q = Q("term", method="POST") & ~Q("term", url="m.ctrip.com/restapi/soa2/11361/json/PushHookTask") \
    & ~Q("term", url="hotelprice.ctrip.com/pricescenter/api/hotelpricescenterws/json/PushHotelPrice") \
    & ~Q("term", url="m.ctrip.com/restapi/soa2/11122/json/PushCaptcha")\
    & ~Q("term", url="m.ctrip.com/restapi/soa2/10994/json/GetFloatUI")\
    & ~Q("term", url="flights.ctrip.com/international/AjaxRequest/SearchFlights/AsyncSearchHandlerSOAII.ashx")\
    & ~Q("term", url="flights.ctrip.com/international/AjaxRequest/AsyncResult/GetRecommendFlight.ashx")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=notice.getHomeNotice")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=notice.getHomeNotice")\
    & ~Q("term", url="exchange-flight.ctrip.com/flt-transferdata-service/ReceiveDataService?RequestType=DomesticClassAV")\
    & ~Q("term", url="m.ctrip.com/restapi/soa2/10957/json/GetJLTaskOrderListV1")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=notice.getListNotice")\
    & ~Q("term", url="m.ctrip.com/restapi/soa2/11361/json/SubmitHookResult")\
    & ~Q("term", url="exchange-flight.ctrip.com/flt-transferdata-service/ReceiveDataService?RequestType=IntlClassAV")\
    & ~Q("term", url="gateway.bus.ctrip.com/open/index.php?param=/api/home&method=partner.orderDetailToken")\
    & ~Q("term", url="m.ctrip.com/restapi/busphp/app/index.php?param=/api/home&method=product.getBusListPage&v=1.0&ref=ctrip.h5&partner=ctrip.app&clientType=Android--hybrid&version=708.002&launchDay=20170510")\
    & ~Q("term", url="m.ctrip.com/restapi/busrecommend/index.php?param=/api/home&method=product.getRecommend&ref=ctrip.h5&partner=ctrip.app&clientType=Android--hybrid&version=708.002&launchDay=20170510")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=product.getFreeCarDesc&ref=ctrip.h5&partner=ctrip.app&clientType=Android--hybrid&version=708.002&launchDay=20170510")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=product.getAirBusPointBus&ref=ctrip.h5&partner=ctrip.app&clientType=Android--hybrid&version=708.002&launchDay=20170510")\
    & ~Q("term", url="english.ctrip.com/flights/Ajax/Next")\
    & ~Q("term", url="m.ctrip.com/restapi/soa2/10957/json/AccountBindV1")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=product.getAirBusPointBus&ref=ctrip.h5&partner=ctrip.app&clientType=Android--hybrid&version=709.003&launchDay=20170510")\
    & ~Q("term", url="trnencrypt.ctrip.com/soaservice/api/json/PushHookTask")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=notice.getListNotice")\
    & ~Q("term", url="m.tieyou.com/index.php?param=/createhtml/getAd.html")\
    & ~Q("term", url="flights.ctrip.com/international/AjaxRequest/Notification.ashx")\
    & ~Q("term", url="m.ctrip.com/restapi/buscommon/index.php?param=/api/home&method=product.getFreeCarDesc&ref=ctrip.h5&partner=ctrip.app&clientType=Android--hybrid&version=709.003&launchDay=20170510")\
    & ~Q("term", url="flights.ctrip.com/international/AjaxRequest/AsyncResult/GetRecommendFlight.ashx")\
    & ~Q("term", uagent="okhttp/3.4.1")\
    & ~Q("term", uagent="Mozilla/4.0")\
    & ~Q("term", uagent="okhttp/2.5.0")\
    & ~Q("term", host="gateway.bus.ctrip.com")\
    & ~Q("term", host="flights.bus.ctrip.com")\
    & ~Q("term", host="hotels.ctrip.com")\
    & ~Q("term", host="ebooking.ctrip.com")\
    & ~Q("term", host="tbooking.ctrip.com")\
    & ~Q("term", host="ebanknotify.payment.ctrip.com")\
    & ~Q("term", host="epush.ctrip.com")\
    & ~Q("term", host="sopenservice.ctrip.com")
    
    
    
    
    
    
    

    #white_file = open("whitewithoutbiaodian.txt", "w")
    white_file = codecs.open("12whitewithoutbiaodian.txt", "w", encoding="utf-8")
    urlset = set()

    while time_start < time_end:
        search_start, search_end = time_start, time_start + datetime.timedelta(hours=time_range)
        print search_start, search_end
        results = search(index_fmt, q, search_start, search_end)
        for result in results:
            postdata = result['postdata'].replace("\r", "").replace("\n", "")
            url = result['host'] + result['uri']
            if url in urlset:
                continue
            else:
                urlset.add(url)
            if 'AppVersionCodeHook' in postdata:
                continue
            # 去除xml
            if postdata.startswith("<"):
             #   print "XML:", postdata
                continue
            # 去除被截断的json
            if postdata.startswith("{") and not postdata.endswith("}"):
             #   print "not json:" + postdata
                continue
#            if postdata.startswith("{"):
#                jsondata = json_decode(postdata)
#                values = get_value_data(jsondata)
#            else:
#                values = get_value_from(postdata)
            try:
                white_file.write(postdata+"\n")
            except:
                print postdata

        time_start = time_start + datetime.timedelta(hours=time_interval + time_range)
        print time_start



