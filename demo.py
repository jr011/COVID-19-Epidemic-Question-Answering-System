import jieba
from SPARQLWrapper import SPARQLWrapper, JSON
from jieba import posseg as pseg
import re
from refo import Predicate, finditer
import Rules

class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

    @staticmethod
    def get_word_objects(sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        return [Word(word.encode('utf-8'), tag) for word, tag in pseg.cut(sentence)]


class Word(object):
    """treated words as objects"""

    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class W(Predicate):
    """object-oriented regex for words"""

    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token.decode('utf-8'))
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if matches:
            return self.action(matches)
        else:
            return ''

def main():
    print("正在初始化...")
    # 连接TDB数据库
    sparql_base = SPARQLWrapper("http://localhost:3030/ep3/query")
    # 加载外部词典
    tagger = Tagger(['dict.txt'])
    print("完成！ \n")

    while True:
        # 输入问题
        print("请输入问题： ")
        default_question = input()
        # try:
        # words = pseg.cut(default_question)
        # print(' '.join('{}/{}'.format(w, t) for w, t in words))
        # 获取wordclass
        seg_list = tagger.get_word_objects(default_question)
        for rule in Rules.MatchRules.rules1:
            # 将规则列表应用到问题上得到查询模板
            query = rule.apply(seg_list)
            if query:
                # 设置查询相关
                sparql_base.setQuery(query)
                sparql_base.setReturnFormat(JSON)
                # 得到返回结果并做转换
                results = sparql_base.query().convert()
                data = str(results)
                patten = re.compile("'value':(.+?)}}")
                list1 = patten.findall(data)
                for i in list1:
                    print("查询结果为：" + i)
                break
        for rule in Rules.MatchRules.rules2:
            query = rule.apply(seg_list)
            if query:
                break

        for rule in Rules.MatchRules.rules3:
            query = None
            # if flag:
            query = rule.apply(seg_list)
            if query:
                break


            # except TypeError:
            #      print("您输入的问题不能识别，请重新输入")
            #      continue
            # except:
            #     print('出错，请debug')


if __name__ == '__main__':
    main()
