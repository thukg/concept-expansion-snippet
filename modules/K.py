import numpy as np
import json
import math
import paras
import pickle
import modules.model_load as model_load

model = None
names = []
grams = []
patterns = []
data = []
mat = []
seed_set = set()

def get_concept_vector(gram):
    vec = []
    for g in gram:
        if g not in model:
            return [], False
        v = model[g]
        vec = v if vec == [] else vec+v
    vec = vec / np.linalg.norm(vec, ord=2)
    return vec, True

def get_similarity(gram1, gram2):
    vec1, p1 = get_concept_vector(gram1)
    vec2, p2 = get_concept_vector(gram2)
    if not p1 or not p2:
        return 0
    return np.dot(vec1, vec2)

def load_data_set():
    global model, data, names, grams, patterns
    names = []
    grams = []
    patterns = []
    data = []
    with open(paras.path_list.tmp, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        for line in lines:
            if line == '':
                continue
            candidate = json.loads(line)
            name = candidate['name']
            gram = candidate['gram']
            num = candidate['gram_num']
            pattern = candidate['pattern']
            S = False
            vec, S = get_concept_vector(gram)
            if S and len(vec):
                names.append(name)
                grams.append(gram)
                patterns.append(pattern)
                data.append(vec)
    data = np.array(data)
    print('Load data complete!', data.shape)

def load_seed_set():
    global seed_set
    seed_set = set()
    with open(paras.path_list.seed, 'r', encoding='utf-8') as f:
        for line in f:
            seed_set.add(line.strip())

def init_score_list():
    global data, seed_set
    score_list = data.shape[0]*[0]
    tot = 0
    for seed in seed_set:
        if seed in names:
            score_list[names.index(seed)] = 1.0
            tot += 1
    print('seed number:', tot)
    return np.array(score_list)

def cal_vector_distance(Top):
    K = 500
    global data, mat, co_occur
    dataT = data.T
    N = data.shape[0]
    M = min(N, Top)
    mat = [[0.0 for j in range(M)] for i in range(N)]
    i = 0
    while i < N:
        weight = np.dot(data[i:i+K], dataT)
        sorted_index = np.argsort(-weight)[:, 0:M]
        for k in range(min(K, N-i)):
            for j in range(M):
                mat[i+k][j] = (weight[k, sorted_index[k, j]], sorted_index[k, j])
        i += min(K, N-i)
        print('Progress:', i/N)

def calc_pow(x, y):
    if x > 0:
        return math.pow(x, y)
    else:
        return -math.pow(-x, y)

def one_round(score_list, max_num, power):
    new_score_list = data.shape[0]*[0]
    tot = data.shape[0]*[0]
    for source, source_score in enumerate(score_list):
        for (weight, target) in mat[source][:max_num]:
            s = source_score * weight
            new_score_list[target] += s
            tot[target] += 1
    max_score = 0.0
    for i in range(len(score_list)):
        if tot[i] > 0:
            new_score_list[i] /= calc_pow(tot[i], power)
        max_score = max(max_score, abs(new_score_list[i]))
    if max_score > 0.0:
        for i in range(len(score_list)):
            new_score_list[i] /= max_score
    return new_score_list

def graph_propagation(score_list, iter_time, max_num, power):
    for i in range(0, iter_time):
        print('Iteration'+str(i+1)+'...')
        score_list = one_round(score_list, max_num, power)
        score_list = np.array(score_list)
    return score_list

def kp_extraction(iter_time=3, max_num=250, power=1):
    global model
    if model is None:
        model = model_load.get_model()
    load_data_set()
    load_seed_set()
    cal_vector_distance(max_num)
    score_list = init_score_list()
    score_list = graph_propagation(score_list, iter_time, max_num, power)
    sorted_list = np.argsort(-score_list)
    with open(paras.path_list.result, 'w', encoding='utf-8') as f:
        for index in sorted_list:
            encode = json.dumps({'name': names[index], 'grams': grams[index], 'score': score_list[index], 'pattern': patterns[index]}, ensure_ascii=False)
            f.write(encode+'\n')
    print('Finished!')
