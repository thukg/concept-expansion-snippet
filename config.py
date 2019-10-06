import os

data = 'data/'
db = 'db/'
model = 'model/'
result = 'result/'
tmp = 'tmp/'

def init():
    if not os.path.exists(data):
        os.mkdirs(data)
    if not os.path.exists(db):
        os.mkdirs(db)
    if not os.path.exists(model):
        os.mkdirs(model)
    if not os.path.exists(result):
        os.mkdirs(result)
    if not os.path.exists(tmp):
        os.mkdirs(tmp)

class PathList:
    def __init__(self):  # default setting
        # word vectors file
        self.zh_model = model+'sgns.baidubaike.bigram-char'
        self.en_model = model+'glove.6B.200d.txt'
        # zh files
        self.jieba_dict = model+'dict.txt'
        self.zh_kp_list = model+'zh_kp_list'
        self.zh_stopwords = model+'zh_stopwords'
        self.snippets_zh = db+'snippets_zh.db'
        # en files
        self.en_kp_list = model+'en_kp_list'
        self.en_stopwords = model+'en_stopwords'
        self.snippets_en = db+'snippets_en.db'
        self.hunpos_model = model+'english.model'
        if os.name == 'nt':  # windows
            self.hunpos_bin = model+'hunpos/hunpos-tag.exe'
        else:
            self.hunpos_bin = model+'hunpos/hupos-tag'
        # paths
        self.result = result+'result'
        self.tmp = tmp+'tmp'
        self.input = tmp+'input'
        self.seed = tmp+'seed'
        # example inputs
        self.input_text = data+'example_text_zh.txt'
        self.input_seed = data+'example_seed_zh.txt'
        #self.input_text = data+'en/captions/EN-Eco'
        #self.input_seed = data+'en/seeds/EN-Eco'
        self.no_seed =  False  # if true, every candidate will be a seed

class Parameter:
    def __init__(self):  # default setting
        self.language = 'zh'
        self.task = 'extract'
        self.iter_time = 100
        self.max_num = -1
        self.threshold = 0.7
        self.decay = 0.8
    
    def set_language(self, language):
        self.language = language
        assert self.language in ['en', 'zh']
    
    def set_task(self, task):
        self.task = task
        assert self.task in ['extract', 'expand']

init()
path_list = PathList()
parameter = Parameter()