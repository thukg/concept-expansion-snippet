# concept-expansion-snippet

This project uses a graph propagation method with pretrained word vectors (GloVe & Word2vec) to do the concept extraction and concept expansion tasks. It supports both Chinese and English.

- **Concept extraction:** Extract concepts from the input text with given seed words.
- **Concept expansion:** Expand concepts by the snippets from search engines (Baidu for Chinese and Google for English) with given seed words.

## Before running the code
1. Decompress `model.zip` to get some basic model files:`unzip model.zip`
2. Decompress the particular HunPos package of `hunpos-1.0-linux.tgz, hunpos-1.0-macosx.tgz, hunpos-1.0-win.zip` according to the operating system, and rename the folder to `hunpos`.
3. Download the following model files, put them in folder `model/` and unzip them:
   - **Candidate concept lists:** [kp_list.zip](http://lfs.aminer.cn/misc/moocdata/toolkit/kp_list.zip)
   - **English word vector:** [glove.6B.zip](http://lfs.aminer.cn/misc/moocdata/toolkit/glove.6B.zip) You will find more information at [GloVe](https://nlp.stanford.edu/projects/glove/)
   - **Chinese word vector:** [sgns.baidubaike.zip](http://lfs.aminer.cn/misc/moocdata/toolkit/sgns.baidubaike.zip) You will find more information at [Chinese-Word-Vectors](https://github.com/Embedding/Chinese-Word-Vectors)
4. modify some path lists in `config.py` if necessary.
5. Install the requirements in `requirements.txt`: `pip install -r requirements.txt`

## Parameters

You can run this project simply by`python main.py` with additional command line parameters. Parameters can be specified in command line or in `config.py`.

Here are the parameters available in command line:

```
input_text: --text
input_seed: --seed, -s
language: --language, -l
task: --task, -t
iter_time: --iter_time, -i
max_num: --max_num, -m
threshold: --threshold, -th
decay: --decay, -d
no_seed: --no_seed, -ns
```

The following path lists can be modified in `config.py`:

```
zh_model, en_model: the word vectors files
jieba_dict
en_stopwords, zh_stopwords
zh_kp_list, en_kp_list: the whole candidate concepts
snippets_zh, snippets_en: the sqlite3 db files to store snippets
hunpos_model, hunpos_bin: nltk hunpos tagger
input, seed, tmp, result
```

## Note

To crawl Google search snippets, you need VPN (for users in Mainland China). 

The crawler may be blocked by anti-crawler programs if you see `get snippet timeout`infomation too many times. Rerun the code will solve this problem most of the time.

You can use other word vectors by modify path lists in `config.py` or rewrite `modules/model_load.py`. It's normal taking a long time and consuming a lot of memory to load the word vector file.

Make sure there is at least one seed word in the input text.