
def create_config_file(config_file_path, creds):
    """
    writes users data to the .config 
    file in the user's home directory 
    """
    
    with open(config_file_path, "w") as token:
        token.write(creds.to_json())
    print(f"created .config file at {config_file_path}")
