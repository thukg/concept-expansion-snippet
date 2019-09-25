import paras
import extract
import expand
import argparse
import os

def preworks():
    if not os.path.exists('db/'):
        os.mkdir('db/')
    if not os.path.exists('result/'):
        os.mkdir('result/')
    if not os.path.exists('tmp/'):
        os.mkdir('tmp/')

def extract_concepts():
    extract.get_concepts()

def expand_concepts():
    expand.get_concepts()

def main():
    if paras.parameter.task == 'extract':
        extract_concepts()
    if paras.parameter.task == 'expand':
        expand_concepts()

def parse():
    parser = argparse.ArgumentParser(description='process some parameters, the whole parameters are in paras.py')
    parser.add_argument('--text', type=str, help='input text file for concept extraction task')
    parser.add_argument('--seed', '-s', type=str, help='seed file for concept extraction/expansion task')
    parser.add_argument('--language', '-l', type=str, choices=['zh', 'en'], help='zh | en')
    parser.add_argument('--task', '-t', type=str, choices=['extract', 'expand'], help='extract | expand')
    parser.add_argument('--iter_time', '-i', type=int, help='iteration time for modules/K.py')
    parser.add_argument('--max_num', '-m', type=int, help='maximun edge number for modules/K.py, "-1" means unlimited')
    parser.add_argument('--threshold', '-th', type=float, help='threshold for modules/K.py')
    parser.add_argument('--decay', '-d', type=float, help='decay for modules/K.py')
    parser.add_argument('noseed', help='no seed file, every candidate will be a seed')
    args = parser.parse_args()
    if args.text:
        paras.path_list.input_text = args.text
    if args.seed:
        paras.path_list.input_seed = args.seed
    if args.language:
        paras.parameter.set_language(args.language)
    if args.task:
        paras.parameter.set_task(args.task)
    if args.iter_time:
        paras.parameter.itertime = args.iter_time
    if args.max_num:
        paras.parameter.max_num = args.max_num
    if args.threshold:
        paras.parameter.threshold = args.threshold
    if args.decay:
        paras.parameter.decay = args.decay
    if args.noseed:
        paras.path_list.no_seed = True

if __name__ == '__main__':
    preworks()
    parse()
    main()