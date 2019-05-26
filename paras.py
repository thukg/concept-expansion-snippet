import os

class PathList:
    def __init__(self):  # default setting
        # word vectors file
        self.zh_model = 'model/sgns.baidubaike.bigram-char'
        self.en_model = 'model/glove.6B.200d.txt'
        # zh files
        self.jieba_dict = 'model/dict.txt'
        self.zh_kp_list = 'model/zh_kp_list'
        self.zh_stopwords = 'model/zh_stopwords'
        self.snippets_zh = 'db/snippets_zh.db'
        # en files
        self.en_kp_list = 'model/en_kp_list'
        self.en_stopwords = 'model/en_stopwords'
        self.snippets_en = 'db/snippets_en.db'
        self.hunpos_model = 'model/english.model'
        if os.name == 'nt':  # windows
            self.hunpos_bin = 'model/hunpos/hunpos-tag.exe'
        else:
            self.hunpos_bin = 'model/hunpos/hupos-tag'
        # paths
        self.result = 'result/result'
        self.tmp = 'tmp/tmp'
        self.input = 'tmp/input'
        self.seed = 'tmp/seed'
        # example inputs
        self.input_text = 'data/example_text.txt'
        self.input_seed = 'data/example_seed.txt'

class Parameter:
    def __init__(self):  # default setting
        self.language = 'zh'
        self.task = 'extract'
        self.iter_time = 3
        self.max_num = 250
        self.power = 1
    
    def set_language(self, language):
        self.language = language
        assert self.language in ['en', 'zh']
    
    def set_task(self, task):
        self.task = task
        assert self.task in ['extract', 'expand']

def create_dirs():
    if not os.path.exists('db/'):
        os.mkdir('db')
    if not os.path.exists('result/'):
        os.mkdir('result')
    if not os.path.exists('tmp/'):
        os.mkdir('tmp')

create_dirs()
path_list = PathList()
parameter = Parameter()