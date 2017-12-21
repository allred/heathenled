#!/usr/bin/env python
import os
from app import create_app

os.environ["FLASK_APP"] = "run.py"
os.environ["APP_SETTINGS"] = "development"

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

if __name__ == '__main__':
    os.system("nosetests")
    app.run()
