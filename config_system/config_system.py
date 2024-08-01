from .oauth_user import authorize_user


def setup_system():
    """authenticates users and creates a .config file"""
    creds = authorize_user()
    return creds

if __name__ == '__main__':
    setup_system()
