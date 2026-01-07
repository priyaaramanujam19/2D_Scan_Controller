import yaml
def load_yaml_file(path='config.yaml'): #Function to load config.yaml
    my_yaml_file = open(path)
    Data = yaml.safe_load(my_yaml_file)
    return Data


