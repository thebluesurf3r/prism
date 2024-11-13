import yaml

def load_config(config_path="config.yaml"):
    """
    Loads the YAML configuration file and returns the configuration as a dictionary.
    """
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

# Example usage:
config = load_config()
print(config['app']['title'])  # Outputs: Prism - Data Analysis Dashboard
print(config['logging']['level'])  # Outputs: INFO
print(config['data']['source_file'])  # Outputs: data/salary_dataset.csv