import os
import json
import pdb
from django.conf import settings

def read_config():
    content = {}
    if os.path.exists(settings.CONFIG_FILE):
        with open(settings.CONFIG_FILE, 'r') as f:
            content = json.load(f)
    return content

def write_config(data):
    #pdb.set_trace()
    content = read_config()
    content.update(data)
    with open(settings.CONFIG_FILE, 'w') as f:
        json.dump(content, f)

def append_log_file_choice(filename):
    content = read_config()
    if 'logfile' not in content:
        content['logfile'] = []
    content['logfile'].append(filename)
    write_config({'logfile': content['logfile']})
    print(read_config())