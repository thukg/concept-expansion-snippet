import pickle
import paras
import numpy as np
import re

def _get_model(f):
    model = {}
    for line in f:
        tmp = line.split(' ')
        if len(tmp) < 3:
            continue
        gram = tmp[0]
        vec = np.array([float(v) for v in tmp[1:-1]])
        model[gram] = vec
    return model

def get_model():
    if paras.parameter.language == 'en':
        with open(paras.path_list.en_model, 'r', encoding='utf-8') as f:
            model = _get_model(f)
    if paras.parameter.language == 'zh':
        with open(paras.path_list.zh_model, 'r', encoding='utf-8') as f:
            model = _get_model(f)
    print('word vector load complete!')
    return model