# !/bin/python3
from project import create_app
import os

app = create_app(1)

if __name__ == "__main__" :
    app.run (host = '0.0.0.0',debug = True)

    
