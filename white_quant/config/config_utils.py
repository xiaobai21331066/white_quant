import yaml
import codecs

def parse_config(file=None):
    with codecs.open(file, encoding='utf-8') as f:
        return yaml.safe_load(f)
