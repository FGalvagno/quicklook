import yaml 
import glob

def load_config():
    config_dict = {}
    cfg_files = glob.glob('./config/*.yml')
    for file in cfg_files:
        f = open(file,'r')
        config_dict.update({f.name[9:-4]: yaml.safe_load(f)})

    return config_dict
