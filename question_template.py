from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as  plt
import re

import numpy
from pyecharts.charts import Map
from selenium import webdriver
from pyecharts import options as opts


Chinese_name = [ '安道尔','安哥拉', '埃塞俄比亚', '科特迪瓦',   '吉布提', '布基纳法索','斯里兰卡', '阿尔及利亚','葡萄牙','加拿大','喀麦隆', '厄立特里亚', '刚果（布）',  '缅甸', '塞浦路斯', '尼日尔', '巴基斯坦', '埃及', '斯洛伐克', '摩纳哥', '乌兹别克斯坦', '利比亚',  '约旦', '巴林', '莫桑比克', '纳米比亚', '加纳', '几内亚', '卢旺达', '坦桑尼亚', '贝宁', '刚果（金）', '利比里亚', '塞拉利昂', '马里','乌拉圭','多哥共和国','塞内加尔', '卢森堡','尼日利亚','沙特阿拉伯','孟加拉国','摩尔多瓦','南非','毛里求斯','肯尼亚','哈萨克斯坦','阿曼','墨西哥', '尼泊尔', '俄罗斯','哥伦比亚','亚美尼亚','洪都拉斯','古巴','新西兰','乌克兰','突尼斯','意大利', '伊朗', '西班牙', '德国', '法国', '美国', '韩国', '丹麦', '瑞士', '挪威', '瑞典', '英国', '荷兰', '日本', '奥地利', '中国', '比利时', '以色列', '捷克', '黎巴嫩', '澳大利亚', '阿联酋', '印度', '罗马尼亚', '马来西亚', '菲律宾', '爱尔兰', '芬兰', '冰岛', '巴西', '斯洛文尼亚', '印度尼西亚', '格鲁吉亚', '阿塞拜疆', '巴拿马', '卡塔尔', '新加坡', '巴勒斯坦', '希腊', '文莱', '波兰', '哥斯达黎加', '多米尼加', '科威特', '秘鲁', '越南', '阿尔巴尼亚', '马耳他', '匈牙利', '北马其顿', '塞尔维亚', '智利', '泰国', '白俄罗斯', '阿富汗', '保加利亚', '克罗地亚', '厄瓜多尔', '巴基斯坦', '拉脱维亚', '波黑', '爱沙尼亚', '玻利维亚', '立陶宛', '阿根廷', '喀麦隆', '土耳其', '摩洛哥', '柬埔寨', '牙买加', '蒙古', '伊拉克', '圣马力诺']
English_name = ['Andorra','Angola','Ethiopia','Côte d\'Ivoire','Djibouti','Burkina Faso','Sri Lanka','Algeria','Portugal','Canada','Cameroon','Eritrea','Congo','Myanmar','Cyprus','Niger','Pakistan','Egypt','Slovakia','Monaco','Uzbekistan','Libya','Jordan','Bahrain','Mozambique','Namibia','Ghana','Guinea','Rwanda','Tanzania','Benin','Dem. Rep. Congo','Liberia','Sierra Leone','Mali','Uruguay','Togo','Senegal','Luxembourg','Nigeria','Saudi Arabia','Bangladesh','Moldova','South Africa','Mauritius','Kenya','Kazakhstan','Oman','Mexico','Nepal','Russia','Colombia','Armenia','Honduras','Cuba','New Zealand','Ukraine','Tunisia','Italy', 'Iran', 'Spain', 'Germany', 'France', 'United States', 'Korea', 'Denmark', 'Switzerland', 'Norway', 'Sweden', 'United Kingdom', 'Netherlands', 'Japan', 'Austria', 'China', 'Belgium', 'Israel', 'Czech Rep.', 'Lebanon', 'Australia', 'United Arab Emirates', 'India', 'Romania', 'Malaysia', 'Philippines', 'Ireland', 'Finland', 'Iceland', 'Brazil', 'Slovenia', 'Indonesia', 'Georgia', 'Azerbaijan', 'Panama', 'Qatar', 'Singapore', 'Palestine', 'Greece', 'Brunei', 'Poland', 'Costa Rica', 'Dominican Rep.', 'Kuwait', 'Peru', 'Vietnam', 'Albania', 'Malta', 'Hungary', 'Macedonia', 'Serbia', 'Chile', 'Thailand', 'Belarus', 'Afghanistan', 'Bulgaria', 'Croatia', 'Ecuador', 'Pakistan', 'Latvia', 'Bosnia and Herz.', 'Estonia', 'Bolivia', 'Lithuania', 'Argentina', 'Cameroon', 'Turkey', 'Morocco', 'Cambodia', 'Jamaica', 'Mongolia', 'Iraq', ' San Marino']

SPARQL_TEM_select = u"{preamble}\n" + \
                    u"SELECT DISTINCT {select} WHERE {{\n" + \
                    u"{expression}\n" + \
                    u"}}\n"

SPARQL_TEM_count = u"{preamble}\n" + \
                   u"SELECT COUNT({select}) WHERE {{\n" + \
                   u"{expression}\n" + \
                   u"}}\n"

SPARQL_ASK_TEM = u"{preamble}\n" + \
                 u"ASK {{\n" + \
                 u"{expression}\n" + \
                 u"}}\n"

SPARQL_PREAMBLE = u"""PREFIX qa: <http://www.kbqa.com/alltime_province_2020_04_04/>
PREFIX qap:<http://www.kbqa.com/alltime_province_2020_04_04/properties#>
PREFIX wor:<http://www.kbqa.com/alltime_world_2020_04_04/properties#>"""


class Template():
    def sw_st_total_confirm(self, x):
        select = u"?confirm"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:total_confirm ?t. ?t qap:total_confirm_num ?confirm."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_confirm(self, x):
        select = u"?confirm"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?confirm."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_total_suspect(self, x):
        select = u"?suspect"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:total_suspect ?t. ?t qap:total_suspect_num ?suspect."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_suspect(self, x):
        select = u"?suspect"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?suspect."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_total_heal(self, x):
        select = u"?heal"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:total_heal ?t. ?t qap:total_heal_num ?heal."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_heal(self, x):
        select = u"?heal"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_heal ?t. ?t qap:today_heal_num ?heal."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_total_dead(self, x):
        select = u"?dead"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:total_dead ?t. ?t qap:total_dead_num ?dead."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_dead(self, x):
        select = u"?dead"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:name {somewhere}. ?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_dead ?t. ?t qap:today_dead_num ?dead."
                break
        for i in x:
            if i.pos == 'ns':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_confirm(self, x):
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_confirm ?t. ?t qap:total_confirm_num ?q. ?Y qap:name ?max. ".format(
                    '"' + i.token.decode('utf_8') + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_suspect(self, x):  # 某天的累计疑似人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num" + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:total_suspect ?t. ?t qap:total_suspect_num ?q. ?Y qap:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_heal(self, x):  # 某天的累计治愈人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num" + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:total_heal ?t. ?t qap:total_heal_num ?q. ?Y qap:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_dead(self, x):  # 某天的累计死亡人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num" + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:total_dead ?t. ?t qap:total_dead_num ?q. ?Y qap:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_confirm(self, x):  # 某天的当天确诊人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?q. ?Y qap:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_suspect(self, x):  # 某天的当天疑似人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?q. ?Y qap:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_heal(self, x):  # 某天的当天治愈人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_heal ?t. ?t qap:today_heal_num ?q. ?Y qap:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_dead(self, x):  # 某天的当天死亡人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y qap:today_dead ?t. ?t qap:today_dead_num ?q. ?Y qap:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def get_region_today_confirm_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_confirm ?c . ?c qap:today_confirm_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_confirm_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_confirm ?c . ?c qap:total_confirm_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_suspect_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_suspect ?c . ?c qap:today_suspect_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_suspect_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_suspect ?c . ?c qap:total_suspect_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_dead_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_dead ?c . ?c qap:today_dead_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_dead_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_dead ?c . ?c qap:total_dead_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_heal_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_heal ?c . ?c qap:today_heal_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_heal_num_above(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_heal ?c . ?c qap:total_heal_num ?d FILTER (?d>{a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_confirm_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_confirm ?c . ?c qap:today_confirm_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_confirm_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_confirm ?c . ?c qap:total_confirm_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_suspect_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_suspect ?c . ?c qap:today_suspect_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_suspect_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_suspect ?c . ?c qap:total_suspect_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_dead_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_dead ?c . ?c qap:today_dead_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_dead_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_dead ?c . ?c qap:total_dead_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_heal_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:today_heal ?c . ?c qap:today_heal_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_heal_num_below(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a qap:lastUpdateTime ?b . ?b qap:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a qap:total_heal ?c . ?c qap:total_heal_num ?d FILTER (?d<={a}) . ?a qap:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_confirm_num_is_zero(self, x):
        return self.get_region_today_confirm_num_below(x)

    def get_region_today_suspect_num_is_zero(self, x):
        return self.get_region_today_suspect_num_below(x)

    def get_region_today_dead_num_is_zero(self, x):
        return self.get_region_today_dead_num_below(x)

    def get_region_today_heal_num_is_zero(self, x):
        return self.get_region_today_heal_num_below(x)

    def get_region_total_confirm_num_is_zero(self, x):
        return self.get_region_total_confirm_num_below(x)

    def get_region_total_suspect_num_is_zero(self, x):
        return self.get_region_total_suspect_num_below(x)

    def get_region_total_dead_num_is_zero(self, x):
        return self.get_region_total_dead_num_below(x)

    def get_region_total_heal_num_is_zero(self, x):
        return self.get_region_total_heal_num_below(x)

    def front_today_confirm(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_today_suspect(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_today_heal(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_heal ?t. ?t qap:today_heal_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_today_dead(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_dead ?t. ?t qap:today_dead_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_confirm(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_confirm ?t. ?t qap:total_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_suspect(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_suspect ?t. ?t qap:total_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_heal(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_heal ?t. ?t qap:total_heal_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_dead(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_dead ?t. ?t qap:total_dead_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_confirm(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_suspect(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_heal(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_heal ?t. ?t qap:today_heal_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_dead(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_dead ?t. ?t qap:today_dead_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_total_confirm_world(self, x):
        select = u"?confirm"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:total_confirm ?t. ?t wor:total_confirm_num ?confirm."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_confirm_world(self, x):
        select = u"?confirm"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?confirm."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_total_suspect_world(self, x):
        select = u"?suspect"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:total_suspect ?t. ?t wor:total_suspect_num ?suspect."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_suspect_world(self, x):
        select = u"?suspect"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?suspect."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_total_heal_world(self, x):
        select = u"?heal"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:total_heal ?t. ?t wor:total_heal_num ?heal."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_heal_world(self, x):
        select = u"?heal"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_heal ?t. ?t wor:today_heal_num ?heal."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_total_dead_world(self, x):
        select = u"?dead"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:total_dead ?t. ?t wor:total_dead_num ?dead."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def sw_st_today_dead_world(self, x):
        select = u"?dead"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:name {somewhere}. ?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_dead ?t. ?t wor:today_dead_num ?dead."
                break
        for i in x:
            if i.pos == 'fo':
                e = e.format(somewhere='"' + i.token.decode("utf-8") + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_confirm_world(self, x):
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_confirm ?t. ?t wor:total_confirm_num ?q. ?Y wor:name ?max. ".format(
                    '"' + i.token.decode('utf_8') + '"')
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_suspect_world(self, x):  # 某天的累计疑似人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num" + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:total_suspect ?t. ?t wor:total_suspect_num ?q. ?Y wor:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_heal_world(self, x):  # 某天的累计治愈人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num" + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:total_heal ?t. ?t wor:total_heal_num ?q. ?Y wor:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_total_dead_world(self, x):  # 某天的累计死亡人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num" + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:total_dead ?t. ?t wor:total_dead_num ?q. ?Y wor:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_confirm_world(self, x):  # 某天的当天确诊人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?q. ?Y wor:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_suspect_world(self, x):  # 某天的当天疑似人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?q. ?Y wor:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_heal_world(self, x):  # 某天的当天治愈人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_heal ?t. ?t wor:today_heal_num ?q. ?Y wor:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_today_dead_world(self, x):  # 某天的当天死亡人数最多的地方是哪里
        select = u"?max"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num " + '"' + i.token.decode(
                    'utf_8') + '"' + ". ?Y wor:today_dead ?t. ?t wor:today_dead_num ?q. ?Y wor:name ?max. "
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def get_region_today_confirm_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_confirm ?c . ?c wor:today_confirm_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_confirm_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_confirm ?c . ?c wor:total_confirm_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_suspect_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_suspect ?c . ?c wor:today_suspect_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_suspect_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_suspect ?c . ?c wor:total_suspect_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_dead_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_dead ?c . ?c wor:today_dead_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_dead_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_dead ?c . ?c wor:total_dead_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_heal_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_heal ?c . ?c wor:today_heal_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_heal_num_above_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_heal ?c . ?c wor:total_heal_num ?d FILTER (?d>{a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_confirm_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_confirm ?c . ?c wor:today_confirm_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_confirm_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_confirm ?c . ?c wor:total_confirm_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_suspect_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_suspect ?c . ?c wor:today_suspect_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_suspect_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_suspect ?c . ?c wor:total_suspect_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_dead_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_dead ?c . ?c wor:today_dead_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_dead_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_dead ?c . ?c wor:total_dead_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_heal_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:today_heal ?c . ?c wor:today_heal_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_total_heal_num_below_world(self, x):
        select = u"?x0"
        e = None
        for i in x:
            if i.pos == 't':
                e = '?a wor:lastUpdateTime ?b . ?b wor:lastUpdateTime_num ' + '"' + i.token.decode(
                    'utf_8') + '"' + '. ?a wor:total_heal ?c . ?c wor:total_heal_num ?d FILTER (?d<={a}) . ?a wor:name ?x0 . '
                break
        for i in x:
            if i.pos == 'm':
                e = e.format(a=str(i.token.decode('utf-8')))

        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression=e)

        print(sparql)
        return sparql

    def get_region_today_confirm_num_is_zero_world(self, x):
        return self.get_region_today_confirm_num_below(x)

    def get_region_today_suspect_num_is_zero_world(self, x):
        return self.get_region_today_suspect_num_below(x)

    def get_region_today_dead_num_is_zero_world(self, x):
        return self.get_region_today_dead_num_below(x)

    def get_region_today_heal_num_is_zero_world(self, x):
        return self.get_region_today_heal_num_below(x)

    def get_region_total_confirm_num_is_zero_world(self, x):
        return self.get_region_total_confirm_num_below(x)

    def get_region_total_suspect_num_is_zero_world(self, x):
        return self.get_region_total_suspect_num_below(x)

    def get_region_total_dead_num_is_zero_world(self, x):
        return self.get_region_total_dead_num_below(x)

    def get_region_total_heal_num_is_zero_world(self, x):
        return self.get_region_total_heal_num_below(x)

    def front_today_confirm_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_today_suspect_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_today_heal_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_heal ?t. ?t wor:today_heal_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_today_dead_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_dead ?t. ?t wor:today_dead_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_confirm_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_confirm ?t. ?t wor:total_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_suspect_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_suspect ?t. ?t wor:total_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_heal_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_heal ?t. ?t wor:total_heal_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def front_total_dead_world(self, x):
        select = u"?sm"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_dead ?t. ?t wor:total_dead_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_confirm_world(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_suspect_world(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_heal_world(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_heal ?t. ?t wor:today_heal_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def max_sm_dead_world(self, x):
        select = u"?time"
        e = None
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_dead ?t. ?t wor:today_dead_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        sparql = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                          select=select,
                                          expression="\t" + e) + "ORDER BY DESC(?q) LIMIT 1"
        print("\nsparql查询语句是：" + "\n" + sparql)
        return sparql

    def draw_front_total_heal(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_heal ?t. ?t qap:total_heal_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_heal(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_heal ?t. ?t qap:today_heal_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_total_dead(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_dead ?t. ?t qap:total_dead_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_dead(self, x):
        print("1")
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_dead ?t. ?t qap:today_dead_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")
        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_total_confirm(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_confirm ?t. ?t qap:total_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_confirm(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")
        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_total_suspect(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:total_suspect ?t. ?t qap:total_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_suspect(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num {}. ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_pie_total_heal(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_heal ?t. ?t qap:total_heal_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_heal(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_heal ?t. ?t qap:today_heal_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_total_dead(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_dead ?t. ?t qap:total_dead_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_dead(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_dead ?t. ?t qap:today_dead_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_total_confirm(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_confirm ?t. ?t qap:total_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_confirm(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_total_suspect(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_suspect ?t. ?t qap:total_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_suspect(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_line_today_suspect(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_line_today_dead(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_dead ?t. ?t qap:today_dead_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_line_today_heal(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_heal ?t. ?t qap:today_heal_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_line_today_confirm(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'ns':
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num ?time. ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?q. ?Y qap:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_front_total_heal_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_heal ?t. ?t wor:total_heal_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_heal_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_heal ?t. ?t wor:today_heal_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_total_dead_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_dead ?t. ?t wor:total_dead_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_dead_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_dead ?t. ?t wor:today_dead_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_total_confirm_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_confirm ?t. ?t wor:total_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_confirm_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_total_suspect_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:total_suspect ?t. ?t wor:total_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_front_today_suspect_world(self, x):
        select = u"?sm ?q"
        e = None
        num = ''
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num {}. ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    '"' + i.token.decode('utf-8') + '"')
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q) LIMIT {}".format(num)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))

        colors = numpy.random.rand(int(num) * 3).reshape(int(num), -1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x=numpy.arange(int(num)), height=list2, alpha=0.8, color=colors, tick_label=list1)
        plt.show()
        return s

    def draw_pie_total_heal_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_heal ?t. ?t wor:total_heal_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_heal_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_heal ?t. ?t wor:today_heal_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")
        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_total_dead_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_dead ?t. ?t wor:total_dead_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_dead_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_dead ?t. ?t wor:today_dead_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_total_confirm_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_confirm ?t. ?t wor:total_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_confirm_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")
        print("查询模板为：" + s)

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_total_suspect_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_suspect ?t. ?t wor:total_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_pie_today_suspect_world(self, x):
        select = u"?sm ?q"
        e = None
        for i in x:
            if i.pos == 't':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print("查询模板为：" + s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list1 = []
        list2 = []
        num = 0
        value = 0
        for n in list:
            if num <= 8 and int(n) != 0:
                list2.append(int(n))
                list1.append(List1[num])
                num = num + 1
            else:
                value += int(n)

        list1.append('其他')
        list2.append(value)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.pie(list2, labels=list1, autopct='%1.1f%%')

        plt.axis('equal')

        plt.legend()

        plt.show()
        return s

    def draw_line_today_suspect_world(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_line_today_dead_world(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_dead ?t. ?t wor:today_dead_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_line_today_heal_world(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_heal ?t. ?t wor:today_heal_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_line_today_confirm_world(self, x):
        select = u"?time ?q"
        e = None
        num = 0
        for i in x:
            if i.pos == 'fo':
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num ?time. ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?q. ?Y wor:name \"{}\". ".format(
                    i.token.decode('utf-8'))
                break
        for i in x:
            if i.pos == 'm':
                num = i.token.decode('utf-8')
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?time) LIMIT {}".format(num)
        print("查询模板为：" + s)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")
        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        List1 = patten.findall(data)
        list1 = List1[::-1]
        print(list1)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        List2 = []
        for n in list:
            List2.append(int(n))
        list2 = List2[::-1]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(list1, list2)
        plt.show()
        return s

    def draw_map_today_confirm(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_confirm ?t. ?t qap:today_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")
        print(s)
        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省确诊病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("确诊病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_map_total_confirm(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_confirm ?t. ?t qap:total_confirm_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")
        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省确诊病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("确诊病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_map_today_suspect(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_suspect ?t. ?t qap:today_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省疑似病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("疑似病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_map_total_suspect(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_suspect ?t. ?t qap:total_suspect_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省疑似病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("疑似病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_map_today_dead(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_dead ?t. ?t qap:today_dead_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省死亡病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("死亡病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_map_total_dead(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_dead ?t. ?t qap:total_dead_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省死亡病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("死亡病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_map_today_heal(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:today_heal ?t. ?t qap:today_heal_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省治愈病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("治愈病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_map_total_heal(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y qap:lastUpdateTime ?Z. ?Z qap:lastUpdateTime_num \"{}\". ?Y qap:total_heal ?t. ?t qap:total_heal_num ?q. ?Y qap:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e) + "ORDER BY DESC(?q)"
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        list = [[list1[i], list2[i]] for i in range(len(list1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "全国各省治愈病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("治愈病例", list, maptype="china")
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_today_suspect(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_suspect ?t. ?t wor:today_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break

        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国疑似病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0),

        )
        map_1.add("疑似病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_total_suspect(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_suspect ?t. ?t wor:total_suspect_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break

        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国疑似病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0),

        )
        map_1.add("疑似病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_today_dead(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_dead ?t. ?t wor:today_dead_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break

        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国死亡病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("死亡病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_total_dead(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_dead ?t. ?t wor:total_dead_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break

        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国死亡病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("死亡病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_today_confirm(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_confirm ?t. ?t wor:today_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)
        print(s)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国确诊病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("确诊病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_total_confirm(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_confirm ?t. ?t wor:total_confirm_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国确诊病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("确诊病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_today_heal(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:today_heal ?t. ?t wor:today_heal_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国治愈病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("治愈病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

    def draw_world_map_total_heal(self, x):
        select = u"?sm ?q"
        e = None
        title = None
        for i in x:
            if i.pos == 't':
                title = i.token.decode('utf-8')
                e = u"?Y wor:lastUpdateTime ?Z. ?Z wor:lastUpdateTime_num \"{}\". ?Y wor:total_heal ?t. ?t wor:total_heal_num ?q. ?Y wor:name ?sm. ".format(
                    i.token.decode('utf-8'))
                break
        s = SPARQL_TEM_select.format(preamble=SPARQL_PREAMBLE,
                                     select=select,
                                     expression="\t" + e)
        sparql = SPARQLWrapper("http://localhost:3030/ep3/sparql")

        sparql.setQuery(s)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = str(results)
        patten = re.compile("'literal', 'value': '(.+?)'}, ")
        list1 = patten.findall(data)
        patten = re.compile("'http://www.w3.org/2001/XMLSchema#integer', 'value': '(.+?)'}}")
        list = patten.findall(data)
        list2 = []
        for n in list:
            list2.append(int(n))
        high = max(list2)
        List1 = []
        List2 = []
        for j in range(len(list1)):
            for i in range(len(Chinese_name)):
                if list1[j] == Chinese_name[i]:
                    List1.append(English_name[i])
                    List2.append(list2[j])

        list = [[List1[i], List2[i]] for i in range(len(List1))]
        map_1 = Map()
        map_1.set_global_opts(
            title_opts=opts.TitleOpts(title=title + "各国治愈病例图"),
            visualmap_opts=opts.VisualMapOpts(max_=high, min_=0)
        )
        map_1.add("治愈病例", list, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        map_1.render('map1.html')
        driver = webdriver.Firefox()
        driver.get("file:///D:\学习\实践\知识工程-疫情\map1.html")
        return s

