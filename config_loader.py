import os


try:
    path = os.environ['CORE_CONFIG']
    from importlib.machinery import SourceFileLoader
    child_config = SourceFileLoader("module", path).load_module().child_config

except:
    from config_child import child_config as child_conf
    child_config = child_conf
