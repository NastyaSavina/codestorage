import yaml

with open(r'fruits.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    fruits_list = yaml.safe_load(file)
    print(fruits_list['dag']['default_args'])