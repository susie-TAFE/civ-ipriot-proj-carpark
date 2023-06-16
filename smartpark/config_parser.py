def parse_config(file_name: str) -> dict:
    """Parse the config file as a string and return the values as a dictionary"""
    import tomli
    with open(file_name, "rb") as config_file:
        config_data = tomli.load(config_file)
    return config_data
