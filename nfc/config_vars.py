import os
from dotenv import load_dotenv

load_dotenv()

ETHEREUM_RECEIVER = os.getenv('ETHEREUM_RECEIVER', '')
ETH_BOLIVIANO_RATE = float(os.getenv('ETH_BOLIVIANO_RATE', '0.00001'))
