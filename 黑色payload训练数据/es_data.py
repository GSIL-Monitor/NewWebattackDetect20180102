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
    time_start = datetime.datetime(2017, 12, 29)   # 起始查询时间
    time_end = datetime.datetime.now()             # 结束查询时间， 默认是当前
    time_interval = 4  # 查询时间间隔, 单位小时
    time_range = 1     # 每次查询时间长度， 单位小时

    # ES 索引
    index_fmt = "nile_ml-%Y.%m.%d"  # nile_ml
    #index_fmt = "pprobe-%Y.%m.%d"   # pprobe

    # 查询条件
    # (nile_ml) 规则没中，中了机器学习  （误报）
    # q = Q("term", is_black=False) & Q("term", rule_result="white") & Q("term", is_ml=True)
    # (nile_ml) 中了黑名单和规则，但是没有中机器学习 （漏报）
    q = (Q("term", is_black=True) | Q("term", rule_result="black")) & Q("term", is_ml=False) & Q("term", method="POST")

    # (pprobe) 只查post数据
    #q = Q("term", method="POST")

    white_file = open("loubao.txt", "w")
    white_file = codecs.open("loubao.txt", "w", encoding="utf-8")

    while time_start < time_end:
        search_start, search_end = time_start, time_start + datetime.timedelta(hours=time_range)
        print search_start, search_end
        results = search(index_fmt, q, search_start, search_end)
        for result in results:
            postdata = result['postdata'].replace("\r", "").replace("\n", "")
            # 去除xml
            if postdata.startswith("<"):
                print "XML:", postdata
                continue
            # 去除被截断的json
            if postdata.startswith("{") and not postdata.endswith("}"):
                print "not json:" + postdata
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
        break



