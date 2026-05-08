
from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL  =os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")
CONN_STR = os.getenv("CONN_STR")