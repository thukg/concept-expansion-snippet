import re
import jieba
import jieba.posseg as pseg
import json
import math
import paras
import pickle

def segment(data):
    res = []
    for line in data:
        line = line.replace(r' ', '').replace('\xa3\xae', '').replace('\x0d', '')
        psgs = pseg.cut(line, False)
        one = []
        for psg in psgs:
            one.append({'flag': psg.flag, 'word': psg.word})
        res.append(one)
    return res

def get_grams(text):
    psgs = pseg.cut(text, False)
    grams = []
    for psg in psgs:
        grams.append(psg.word)
    return grams

def phrase_in_lists(lists, phrase):
    t1 = 0
    t2 = len(lists) - 1
    while t1 < t2:
        t3 = (t1 + t2) // 2
        if phrase > lists[t3]:
            t1 = t3 + 1
        else:
            t2 = t3
    if phrase == lists[t1]:
        return True
    else:
        return False

def is_noun(flag):
    if re.match(r'^(@(([av]?n[rstz]?)|l|a|v))*(@(([av]?n[rstz]?)|l))$', flag) is not None:
        return True
    else:
        return False

def pattern_filter(lists, data, stopwords):
    res = []
    word_set = set()
    tot = 0
    for psgs in data:
        n = len(psgs)
        for i in range(0, n):
            flags = []
            words = []
            flag_str = ''
            word_str = ''
            for j in range(0, 3):
                if i + j >= n or psgs[i+j]['word'] in words or psgs[i+j]['word'] in stopwords:
                    continue
                flags.append(psgs[i+j]['flag'])
                words.append(psgs[i+j]['word'])
                flag_str += '@' + psgs[i+j]['flag']
                word_str += psgs[i+j]['word']
                if is_noun(flag_str) and word_str not in word_set:
                    word_set.add(word_str)
                    if phrase_in_lists(lists, word_str):
                        res.append([flags.copy(), words.copy()])
                    tot += 1
    print('phrases:', tot, 'in_lists:', len(res))
    return res

def json_gen(data):
    names = []
    grams = []
    gram_num = []
    patterns = []
    tot = 0
    for flags, words in data:
        if len(words) == 1 and len(words[0]) < 2:
            continue
        names.append(''.join(words))
        grams.append(words)
        gram_num.append(len(words))
        patterns.append(' '.join(flags))
        tot += 1
    print('json_gen:', tot)
    with open(paras.path_list.tmp, 'w', encoding='utf-8') as f:
        for i in range(len(names)):
            encode = json.dumps(
                {'name': names[i], 'gram': grams[i], 'gram_num': gram_num[i], 'pattern': patterns[i]}, ensure_ascii=False)
            f.write(encode + '\n')

def work():
    jieba.load_userdict(paras.path_list.jieba_dict)
    with open(paras.path_list.zh_stopwords, 'r', encoding='utf-8') as f:
        stopwords = set(f.read().split('\n'))
    with open(paras.path_list.zh_kp_list, 'r', encoding='utf-8') as f:
        lists = f.read().split('\n')
        print('load kp_list done.')
    with open(paras.path_list.input, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
        res1 = segment(data)
        res2 = pattern_filter(lists, res1, stopwords)
        json_gen(res2)
    print('prework done.')
