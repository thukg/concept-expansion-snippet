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
    K.kp_extraction()

if __name__ == '__main__':
    get_concepts()