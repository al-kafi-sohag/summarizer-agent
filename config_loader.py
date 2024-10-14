import os
import sys
import yaml

def load_config(config_path='config.yaml'):
    if not os.path.exists(config_path):
        print(f"Configuration file '{config_path}' not found.")
        sys.exit(1)
    with open(config_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as e:
            print(f"Error parsing the configuration file: {e}")
            sys.exit(1)