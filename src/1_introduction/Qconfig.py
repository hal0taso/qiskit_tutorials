import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APItoken = os.environ.get("APItoken")
config = {'url': 'https://quantumexperience.ng.bluemix.net/api'}

if 'APItoken' not in locals():
    raise Exception('Please set up your access token. See Qconfig.py.')

