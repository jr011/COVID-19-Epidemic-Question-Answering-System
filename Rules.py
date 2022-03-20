from refo import Star, Any
from demo import Rule, W
from question_template import Template

t = Template()


class MatchRules ():
    rules1 = [
        # 国家
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("全部") + W("确诊"),
             # 到某天为止，某地全部确诊人数
             action=t.sw_st_total_confirm_world),
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("全部") + W("疑诊"),
             # 到某天为止，某地全部疑诊人数
             action=t.sw_st_total_suspect_world),
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("全部") + W("治愈"),
             # 到某天为止，某地全部治愈人数
             action=t.sw_st_total_heal_world),
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("全部") + W("死亡"),
             # 到某天为止，某地全部死亡人数
             action=t.sw_st_total_dead_world),
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("确诊") |
                       W(pos="t") + W("当天") + W(pos='fo') + Star(Any(), greedy=False) + W("确诊"),
             # 某地某天确诊人数
             action=t.sw_st_today_confirm_world),
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("疑诊") |
                       W(pos="t") + W("当天") + W(pos='fo') + Star(Any(), greedy=False) + W("疑诊"),
             # 某地某天疑诊人数
             action=t.sw_st_today_suspect_world),
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("治愈") |
                       W(pos="t") + W("当天") + W(pos='fo') + Star(Any(), greedy=False) + W("治愈"),
             # 某地某天治愈人数
             action=t.sw_st_today_suspect_world),
        Rule(condition=W(pos="t") + W(pos='fo') + Star(Any(), greedy=False) + W("死亡") |
                       W(pos="t") + W("当天") + W(pos='fo') + Star(Any(), greedy=False) + W("死亡"),
             # 某地某天死亡人数
             action=t.sw_st_today_suspect_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("确诊") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的当天确诊人数最多的地方是哪里？
             action=t.max_today_confirm_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累计") | W("累积")) + W("确诊") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的累计确诊人数最多的地方是哪里
             action=t.max_total_confirm_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累计") | W("累积")) + W("疑似") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的累计疑似人数最多的地方是哪里
             action=t.max_total_suspect_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累计") | W("累积"))+ W("治愈") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的累计治愈人数最多的地方是哪里
             action=t.max_total_heal_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累计") | W("累积")) + W("死亡") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的累计死亡人数最多的地方是哪里
             action=t.max_total_dead_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("确诊") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的当天确诊人数最多的地方是哪里
             action=t.max_today_confirm_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("疑似") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的当天疑似人数最多的地方是哪里
             action=t.max_today_suspect_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("治愈") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的当天治愈人数最多的地方是哪里
             action=t.max_today_heal_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("死亡") + W("人数最多") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),  # 某天的当天死亡人数最多的地方是哪里
             action=t.max_today_dead_world),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天确诊人数高于多少的地方是哪里？
             action=t.get_region_today_confirm_num_above_world),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天疑诊人数高于多少的地方是哪里？
             action=t.get_region_today_suspect_num_above_world),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天治愈人数高于多少的地方是哪里？
             action=t.get_region_today_heal_num_above_world),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天死亡人数高于多少的地方是哪里？
             action=t.get_region_today_dead_num_above_world),
        Rule(condition=W(pos="t") + (W("累计") | W("累积")) + W("确诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的累计确诊人数高于多少的地方是哪里？
             action=t.get_region_total_confirm_num_above_world),
        Rule(condition=W(pos="t") + (W("累计") | W("累积")) + W("疑诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的累计疑诊人数高于多少的地方是哪里？
             action=t.get_region_total_suspect_num_above_world),
        Rule(condition=W(pos="t") + (W("累计") | W("累积")) + W("治愈") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的累计治愈人数高于多少的地方是哪里？
             action=t.get_region_total_heal_num_above_world),
        Rule(condition=W(pos="t") + (W("累计") | W("累积")) + W("死亡") + Star(Any(), greedy=False) + W("高于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的累计死亡人数高于多少的地方是哪里？
             action=t.get_region_total_dead_num_above_world),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("低于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天确诊人数低于多少的地方是哪里？
             action=t.get_region_today_confirm_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("低于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天疑诊人数低于多少的地方是哪里？
             action=t.get_region_today_suspect_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("低于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天治愈人数低于多少的地方是哪里？
             action=t.get_region_today_heal_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("低于") + W(pos='m') + Star(Any(),
                                                                                                                greedy=False) + W(
            "国家"),
             # 某天的当天死亡人数低于多少的地方是哪里？
             action=t.get_region_today_dead_num_below_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + W("低于") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累计确诊人数低于多少的地方是哪里？
             action=t.get_region_total_confirm_num_below_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + W("低于") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累计疑诊人数低于多少的地方是哪里？
             action=t.get_region_total_suspect_num_below_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + W("低于") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累计治愈人数低于多少的地方是哪里？
             action=t.get_region_total_heal_num_below_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + W("低于") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累计死亡人数低于多少的地方是哪里？
             action=t.get_region_total_dead_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(Any(),
                                                                                                             greedy=False) + W(
            "国家"),
             # 某天的当天确诊人数为0的地方是哪里？
             action=t.get_region_today_confirm_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(Any(),
                                                                                                             greedy=False) + W(
            "国家"),
             # 某天的当天疑似人数为0的地方是哪里？
             action=t.get_region_today_suspect_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(Any(),
                                                                                                             greedy=False) + W(
            "国家"),
             # 某天的当天治愈人数为0的地方是哪里？
             action=t.get_region_today_heal_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(Any(),
                                                                                                             greedy=False) + W(
            "国家"),
             # 某天的当天死亡人数为0的地方是哪里？
             action=t.get_region_today_dead_num_below_world),
        Rule(
            condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(
                Any(), greedy=False) + W("国家"),
            # 某天的累计确诊人数为0的地方是哪里？
            action=t.get_region_total_confirm_num_below_world),
        Rule(
            condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(
                Any(), greedy=False) + W("国家"),
            # 某天的累计疑似人数为0的地方是哪里？
            action=t.get_region_total_suspect_num_below_world),
        Rule(
            condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(
                Any(), greedy=False) + W("国家"),
            # 某天的累计治愈人数为0的地方是哪里？
            action=t.get_region_total_heal_num_below_world),
        Rule(
            condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + (W("0") | W("零")) + Star(
                Any(), greedy=False) + W("国家"),
            # 某天的累计死亡人数为0的地方是哪里？
            action=t.get_region_total_dead_num_below_world),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天确诊人数前多少的地方是哪里？
             action=t.front_today_confirm_world),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天疑诊人数前多少的地方是哪里？
             action=t.front_today_suspect_world),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天治愈人数前多少的地方是哪里？
             action=t.front_today_heal_world),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天死亡人数前多少的地方是哪里？
             action=t.front_today_dead_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积确诊人数前多少的地方是哪里？
             action=t.front_total_confirm_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积疑诊人数前多少的地方是哪里？
             action=t.front_total_suspect_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积治愈人数前多少的地方是哪里？
             action=t.front_total_heal_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积死亡人数前多少的地方是哪里？
             action=t.front_total_dead_world),
        Rule(condition=W(pos='fo') + W('哪天') + W("确诊") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天确诊人数最多
             action=t.max_sm_confirm_world),
        Rule(condition=W(pos='fo') + W('哪天') + W("疑诊") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天疑诊人数最多
             action=t.max_sm_confirm_world),
        Rule(condition=W(pos='fo') + W('哪天') + W("治愈") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天治愈人数最多
             action=t.max_sm_confirm_world),
        Rule(condition=W(pos='fo') + W('哪天') + W("死亡") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天死亡人数最多
             action=t.max_sm_confirm_world),
        # 省份
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("全部") + W("确诊"),
             # 到某天为止，某地全部确诊人数
             action=t.sw_st_total_confirm),
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("全部") + W("疑诊"),
             # 到某天为止，某地全部疑诊人数
             action=t.sw_st_total_suspect),
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("全部") + W("治愈"),
             # 到某天为止，某地全部治愈人数
             action=t.sw_st_total_heal),
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("全部") + W("死亡"),
             # 到某天为止，某地全部死亡人数
             action=t.sw_st_total_dead),
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("确诊") |
                       W(pos="t") + W("当天") + W(pos='ns') + Star(Any(), greedy=False) + W("确诊"),
             # 某地某天确诊人数
             action=t.sw_st_today_confirm),
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("疑诊") |
                       W(pos="t") + W("当天") + W(pos='ns') + Star(Any(), greedy=False) + W("疑诊"),
             # 某地某天疑诊人数
             action=t.sw_st_today_suspect),
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("治愈") |
                       W(pos="t") + W("当天") + W(pos='ns') + Star(Any(), greedy=False) + W("治愈"),
             # 某地某天治愈人数
             action=t.sw_st_today_heal),
        Rule(condition=W(pos="t") + W(pos='ns') + Star(Any(), greedy=False) + W("死亡") |
                       W(pos="t") + W("当天") + W(pos='ns') + Star(Any(), greedy=False) + W("死亡"),
             # 某地某天死亡人数
             action=t.sw_st_today_dead),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("确诊") + W("人数最多"),
             # 某天的当天确诊人数最多的地方是哪里？
             action=t.max_today_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("确诊") + W("人数最多"),
             # 某天的累计确诊人数最多的地方是哪里
             action=t.max_total_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("疑似") + W("人数最多"),
             # 某天的累计疑似人数最多的地方是哪里
             action=t.max_total_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("治愈") + W("人数最多"),
             # 某天的累计治愈人数最多的地方是哪里
             action=t.max_total_heal),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("死亡") + W("人数最多"),
             # 某天的累计死亡人数最多的地方是哪里
             action=t.max_total_dead),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("确诊") + W("人数最多"),
             # 某天的当天确诊人数最多的地方是哪里
             action=t.max_today_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("疑似") + W("人数最多"),
             # 某天的当天疑似人数最多的地方是哪里
             action=t.max_today_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("治愈") + W("人数最多"),
             # 某天的当天治愈人数最多的地方是哪里
             action=t.max_today_heal),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + W("死亡") + W("人数最多"),
             # 某天的当天死亡人数最多的地方是哪里
             action=t.max_today_dead),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的当天确诊人数高于多少的地方是哪里？
             action=t.get_region_today_confirm_num_above),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的当天疑诊人数高于多少的地方是哪里？
             action=t.get_region_today_suspect_num_above),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的当天治愈人数高于多少的地方是哪里？
             action=t.get_region_today_heal_num_above),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的当天死亡人数高于多少的地方是哪里？
             action=t.get_region_today_dead_num_above),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的累计确诊人数高于多少的地方是哪里？
             action=t.get_region_total_confirm_num_above),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的累计疑诊人数高于多少的地方是哪里？
             action=t.get_region_total_suspect_num_above),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的累计治愈人数高于多少的地方是哪里？
             action=t.get_region_total_heal_num_above),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + W("高于") + W(pos='m'),
             # 某天的累计死亡人数高于多少的地方是哪里？
             action=t.get_region_total_dead_num_above),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的当天确诊人数低于多少的地方是哪里？
             action=t.get_region_today_confirm_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的当天疑诊人数低于多少的地方是哪里？
             action=t.get_region_today_suspect_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的当天治愈人数低于多少的地方是哪里？
             action=t.get_region_today_heal_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的当天死亡人数低于多少的地方是哪里？
             action=t.get_region_today_dead_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的累计确诊人数低于多少的地方是哪里？
             action=t.get_region_total_confirm_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的累计疑诊人数低于多少的地方是哪里？
             action=t.get_region_total_suspect_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的累计治愈人数低于多少的地方是哪里？
             action=t.get_region_total_heal_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + W("低于") + W(pos='m'),
             # 某天的累计死亡人数低于多少的地方是哪里？
             action=t.get_region_total_dead_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的当天确诊人数为0的地方是哪里？
             action=t.get_region_today_confirm_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的当天疑似人数为0的地方是哪里？
             action=t.get_region_today_suspect_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的当天治愈人数为0的地方是哪里？
             action=t.get_region_today_heal_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的当天死亡人数为0的地方是哪里？
             action=t.get_region_today_dead_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的累计确诊人数为0的地方是哪里？
             action=t.get_region_total_confirm_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的累计疑似人数为0的地方是哪里？
             action=t.get_region_total_suspect_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的累计治愈人数为0的地方是哪里？
             action=t.get_region_total_heal_num_below),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + (W("0") | W("零")),
             # 某天的累计死亡人数为0的地方是哪里？
             action=t.get_region_total_dead_num_below),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天确诊人数前多少的地方是哪里？
             action=t.front_today_confirm),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天疑诊人数前多少的地方是哪里？
             action=t.front_today_suspect),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天治愈人数前多少的地方是哪里？
             action=t.front_today_heal),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天死亡人数前多少的地方是哪里？
             action=t.front_today_dead),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积确诊人数前多少的地方是哪里？
             action=t.front_total_confirm),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积疑诊人数前多少的地方是哪里？
             action=t.front_total_suspect),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积治愈人数前多少的地方是哪里？
             action=t.front_total_heal),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积死亡人数前多少的地方是哪里？
             action=t.front_total_dead),
        Rule(condition=W(pos='ns') + W('哪天') + W("确诊") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天确诊人数最多
             action=t.max_sm_confirm),
        Rule(condition=W(pos='ns') + W('哪天') + W("疑诊") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天疑诊人数最多
             action=t.max_sm_confirm),
        Rule(condition=W(pos='ns') + W('哪天') + W("治愈") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天治愈人数最多
             action=t.max_sm_confirm),
        Rule(condition=W(pos='ns') + W('哪天') + W("死亡") + Star(Any(), greedy=False) + W("人数最多"),
             # 某地哪天的当天死亡人数最多
             action=t.max_sm_confirm)
    ]

    rules2 = [
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积确诊人数前多少的地方是哪里？
             action=t.draw_front_total_confirm_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积疑诊人数前多少的地方是哪里？
             action=t.draw_front_total_suspect_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积治愈人数前多少的地方是哪里？
             action=t.draw_front_total_heal_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + W("前") + W(
            pos='m') + Star(Any(), greedy=False) + W("国家"),
             # 某天的累积死亡人数前多少的地方是哪里？
             action=t.draw_front_total_dead_world),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天确诊人数前多少的地方是哪里？
             action=t.draw_front_today_confirm_world),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天疑诊人数前多少的地方是哪里？
             action=t.draw_front_today_suspect_world),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天治愈人数前多少的地方是哪里？
             action=t.draw_front_today_heal_world),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("前") + W(pos='m') + Star(Any(),
                                                                                                               greedy=False) + W(
            "国家"),
             # 某天的当天死亡人数前多少的地方是哪里？
             action=t.draw_front_today_dead_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("国家") + (W("累积") | W("累计")) + W("确诊") + Star(Any(),
                                                                                                     greedy=False) ,
             # 到某天为止，各国家的累积确诊人数所占比例？
             action=t.draw_pie_total_confirm_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("国家") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(),
                                                                                                     greedy=False) ,
             # 到某天为止，各国家的累积疑诊人数所占比例？
             action=t.draw_pie_total_suspect_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("国家") + (W("累积") | W("累计")) + W("治愈") + Star(Any(),
                                                                                                     greedy=False) ,
             # 到某天为止，各国家的累积治愈人数所占比例？
             action=t.draw_pie_total_heal_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("国家") + (W("累积") | W("累计")) + W("死亡") + Star(Any(),
                                                                                                     greedy=False),
             # 到某天为止，各国家的累积死亡人数所占比例？
             action=t.draw_pie_total_dead_world),

        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("确诊") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),
             # 某天的累积确诊人数？
             action=t.draw_pie_today_confirm_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("疑诊") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),
             # 某天的累积疑诊人数？
             action=t.draw_pie_today_suspect_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("治愈") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),
             # 某天的累积治愈人数？
             action=t.draw_pie_today_heal_world),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("死亡") + Star(Any(),
                                                                                                     greedy=False) + W(
            "国家"),
             # 某天的累积死亡人数？
             action=t.draw_pie_today_dead_world),

        Rule(condition=W(pos="fo") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("确诊"),
             # 某地最近几天的确诊人数
             action=t.draw_line_today_confirm_world),
        Rule(condition=W(pos="fo") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("疑诊"),
             # 某地最近几天的疑诊人数
             action=t.draw_line_today_suspect_world),
        Rule(condition=W(pos="fo") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("治愈"),
             # 某地最近几天的治愈人数
             action=t.draw_line_today_heal_world),
        Rule(condition=W(pos="fo") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("死亡"),
             # 某地最近几天的死亡人数
             action=t.draw_line_today_dead_world),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("确诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积确诊人数前多少的地方是哪里？
             action=t.draw_front_total_confirm),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积疑诊人数前多少的地方是哪里？
             action=t.draw_front_total_suspect),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("治愈") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积治愈人数前多少的地方是哪里？
             action=t.draw_front_total_heal),
        Rule(condition=W(pos="t") + (W("累积") | W("累计")) + W("死亡") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的累积死亡人数前多少的地方是哪里？
             action=t.draw_front_total_dead),
        Rule(condition=W(pos="t") + W("当天") + W("确诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天确诊人数前多少的地方是哪里？
             action=t.draw_front_today_confirm),
        Rule(condition=W(pos="t") + W("当天") + W("疑诊") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天疑诊人数前多少的地方是哪里？
             action=t.draw_front_today_suspect),
        Rule(condition=W(pos="t") + W("当天") + W("治愈") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天治愈人数前多少的地方是哪里？
             action=t.draw_front_today_heal),
        Rule(condition=W(pos="t") + W("当天") + W("死亡") + Star(Any(), greedy=False) + W("前") + W(pos='m'),
             # 某天的当天死亡人数前多少的地方是哪里？
             action=t.draw_front_today_dead),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("确诊"),
             # 某天的累积确诊人数？
             action=t.draw_pie_total_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("疑诊"),
             # 某天的累积疑诊人数？
             action=t.draw_pie_total_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("治愈"),
             # 某天的累积治愈人数？
             action=t.draw_pie_total_heal),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("死亡"),
             # 某天的累积死亡人数？
             action=t.draw_pie_total_dead),

        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("确诊"),
             # 某天的累积确诊人数？
             action=t.draw_pie_today_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("疑诊"),
             # 某天的累积疑诊人数？
             action=t.draw_pie_today_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("治愈") ,
             # 某天的累积治愈人数？
             action=t.draw_pie_today_heal),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("当天")) + W("死亡") ,
             # 某天的累积死亡人数？
             action=t.draw_pie_today_dead),

        Rule(condition=W(pos="ns") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("确诊"),
             # 某地最近几天的确诊人数
             action=t.draw_line_today_confirm),
        Rule(condition=W(pos="ns") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("疑诊"),
             # 某地最近几天的疑诊人数
             action=t.draw_line_today_suspect),
        Rule(condition=W(pos="ns") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("治愈"),
             # 某地最近几天的治愈人数
             action=t.draw_line_today_heal),
        Rule(condition=W(pos="ns") + W("最近") + W(pos="m") + Star(Any(), greedy=False) + W("死亡"),
             # 某地最近几天的死亡人数
             action=t.draw_line_today_dead)
    ]

    rules3 = [
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("国家") + W("确诊"),
             # 某天的当天各国家确诊人数？
             action=t.draw_world_map_today_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("国家") + W("疑诊"),
             # 某天的当天各国家疑诊人数？(国家)
             action=t.draw_world_map_today_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("国家") + W("死亡"),
             # 某天的当天各国家死亡人数？(国家)
             action=t.draw_world_map_today_dead),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("国家") + W("治愈"),
             # 某天的当天各国家治愈人数？(国家)
             action=t.draw_world_map_today_heal),

        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + Star(Any(), greedy=False) + W("国家") + (W("累积") | W("累计")) + W("确诊"),  # 某天的累积确诊人数？(国家)
             action=t.draw_world_map_total_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + Star(Any(), greedy=False) + W("国家") + W("疑诊"),  # 某天的累积疑诊人数？(国家)
             action=t.draw_world_map_total_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + Star(Any(), greedy=False) + W("国家") + W("死亡"),  # 某天的累积死亡人数？(国家)
             action=t.draw_world_map_total_dead),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + Star(Any(), greedy=False) + W("国家") + W("治愈"),  # 某天的累积治愈人数？(国家)
             action=t.draw_world_map_total_heal),

        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("省份") + W("确诊"),  # 某天的当天各省份确诊人数？
             action=t.draw_map_today_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("省份") + W("疑诊"),  # 某天的当天各省份疑诊人数？
             action=t.draw_map_today_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("省份") + W("死亡"),  # 某天的当天各省份死亡人数？
             action=t.draw_map_today_dead),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + W("当天") + Star(Any(), greedy=False) + W("省份") + W("治愈"),  # 某天的当天各省份治愈人数？
             action=t.draw_map_today_heal),

        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("确诊"),  # 某天的累积确诊人数？
             action=t.draw_map_total_confirm),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("疑诊"),  # 某天的累积疑诊人数？
             action=t.draw_map_total_suspect),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("死亡"),  # 某天的累积死亡人数？
             action=t.draw_map_total_dead),
        Rule(condition=W(pos="t") + Star(Any(), greedy=False) + (W("累积") | W("累计")) + W("治愈"),  # 某天的累积治愈人数？
             action=t.draw_map_total_heal),
    ]