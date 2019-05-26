import re
import nltk
import inflect
import json
import paras
import pickle
from nltk.tag.hunpos import HunposTagger

conversion = None

def segment(data, pos_tagger):
    res = []
    for line in data:
        line = line.replace('\xa3\xae', '').replace('\x0d', '')
        tmp = nltk.word_tokenize(line)
        seg = []
        for word in tmp:
            if all(ord(c) < 128 for c in word):
                seg.append(word)
        psgs = pos_tagger.tag(seg)
        one = []
        for psg in psgs:
            flag = bytes.decode(psg[1])
            one.append({'flag': flag, 'word': psg[0]})
        res.append(one)
    return res

def get_grams(text):
    return nltk.word_tokenize(text)

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
    flag = re.sub('JJ[RS]?', 'JJ', flag)
    flag = re.sub('NN[SP(PS)]?', 'NN', flag)
    if re.match(r'^((@(JJ|NN))+|(@(JJ|NN))*(@(NN|IN))?(@(JJ|NN))*)@NN$', flag) is not None:
        return True
    else:
        return False

def to_singular(flag, word):
    if flag in ['NN', 'NNS', 'NNP', 'NNPS']:
        tmp = conversion.singular_noun(word)
        if tmp != False:
            word = tmp
    return word

def pattern_filter(lists, data, stopwords):
    res = []
    phrase_set = set()
    tot = 0
    for psgs in data:
        n = len(psgs)
        for i in range(0, n):
            flags = []
            words = []
            flag_str = ''
            word_str = ''
            for j in range(0, 4):
                if i + j >= n or psgs[i+j]['word'] in words or psgs[i+j]['word'] in stopwords:
                    continue
                flags.append(psgs[i+j]['flag'])
                words.append(psgs[i+j]['word'])
                flag_str += '@' + psgs[i+j]['flag']
                tmp = words[:-1] + [to_singular(flags[-1], words[-1])]
                phrase = ' '.join(tmp)
                if is_noun(flag_str) and phrase not in phrase_set:
                    phrase_set.add(phrase)
                    if phrase_in_lists(lists, phrase):
                        res.append([flags.copy(), tmp.copy()])
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
        names.append(' '.join(words))
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
    global conversion
    pos_tagger = HunposTagger(path_to_model=paras.path_list.hunpos_model, path_to_bin=paras.path_list.hunpos_bin)
    conversion = inflect.engine()
    with open(paras.path_list.en_stopwords, 'r', encoding='utf-8') as f:
        stopwords = set(f.read().split('\n'))
    with open(paras.path_list.en_kp_list, 'r', encoding='utf-8') as f:
        lists = f.read().split('\n')
        print('load kp_list done.')
    with open(paras.path_list.input, 'r', encoding='utf-8') as f:
        data = []
        for line in f.read().split('\n'):
            if line == '':
                continue
            data.append(line.lower())
        res1 = segment(data, pos_tagger)
        res2 = pattern_filter(lists, res1, stopwords)
        json_gen(res2)
        print('prework done.')
    pos_tagger.close()
