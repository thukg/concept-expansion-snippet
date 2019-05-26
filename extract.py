import paras
import shutil

def get_concepts():
    import modules.K as K
    if paras.parameter.language == 'en':
        import modules.prework_en as prework
    if paras.parameter.language == 'zh':
        import modules.prework_zh as prework
    shutil.copy(paras.path_list.input_text, paras.path_list.input)
    shutil.copy(paras.path_list.input_seed, paras.path_list.seed)
    prework.work()
    K.kp_extraction(iter_time=paras.parameter.iter_time, max_num=paras.parameter.max_num, power=paras.parameter.power)

if __name__ == '__main__':
    get_concepts()