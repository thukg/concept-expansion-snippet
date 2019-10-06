import config
import shutil

def get_concepts():
    import modules.K as K
    if config.parameter.language == 'en':
        import modules.prework_en as prework
    if config.parameter.language == 'zh':
        import modules.prework_zh as prework
    shutil.copy(config.path_list.input_text, config.path_list.input)
    shutil.copy(config.path_list.input_seed, config.path_list.seed)
    prework.work()
    K.kp_extraction()

if __name__ == '__main__':
    get_concepts()