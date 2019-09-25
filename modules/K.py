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
    if not paras.path_list.no_seed:
        with open(paras.path_list.seed, 'r', encoding='utf-8') as f:
            for line in f:
                seed_set.add(line.strip())

def init_score_list():
    global data, seed_set
    score_list = np.zeros(data.shape[0])
    tot = 0
    if paras.path_list.no_seed:
        for i in range(len(names)):
            score_list[i] = 1.0
            tot += 1
    else:
        for seed in seed_set:
            if seed in names:
                score_list[names.index(seed)] = 1.0
                tot += 1
    print('Seed number in candidates:', tot)
    return score_list

def cal_vector_distance(max_num, t):
    K = 500
    global data, mat, co_occur
    dataT = data.T
    N = data.shape[0]
    M = N if max_num == -1 else min(N, max_num)
    mat = [[] for i in range(N)]
    i = 0
    while i < N:
        weight = np.dot(data[i:i+K], dataT)
        sorted_index = np.argsort(-weight)[:, 0:M]
        for k in range(min(K, N-i)):
            for j in range(M):
                w = weight[k, sorted_index[k, j]]
                tar = sorted_index[k, j]
                if w > t:
                    mat[i+k].append([w, tar])
        i += min(K, N-i)
        print('Progress:', i/N)

def calc_pow(x, y):
    if x > 0:
        return math.pow(x, y)
    else:
        return -math.pow(-x, y)

def one_round(score_list):
    new_score_list = np.zeros(data.shape[0])
    for source, score in enumerate(score_list):
        if score != 0.0:
            for (weight, target) in mat[source]:
                s = score * weight
                new_score_list[target] += s
    new_score_list /= np.max(new_score_list)
    return new_score_list

def graph_propagation(score_list, iter_time, decay):
    final_score_list = score_list
    for i in range(0, iter_time):
        print('Iteration round:', str(i+1))
        score_list = one_round(score_list)
        final_score_list += score_list * calc_pow(decay, i)
    #return score_list
    return final_score_list

def kp_extraction():
    p = paras.parameter
    iter_time, max_num, threshold, decay = p.iter_time, p.max_num, p.threshold, p.decay
    global model
    if model is None:
        model = model_load.get_model()
    load_data_set()
    load_seed_set()
    cal_vector_distance(max_num, threshold)
    score_list = init_score_list()
    score_list = graph_propagation(score_list, iter_time, decay)
    sorted_list = np.argsort(-score_list)
    with open(paras.path_list.result, 'w', encoding='utf-8') as f:
        for index in sorted_list:
            encode = json.dumps({'name': names[index], 'grams': grams[index], 'score': score_list[index], 'pattern': patterns[index]}, ensure_ascii=False)
            f.write(encode+'\n')
    print('Finished!')
