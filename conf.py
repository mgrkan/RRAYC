import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
SAMPLE_DIR = os.path.join(DATA_DIR, "samples")
SAMPLE_INPUTS = os.path.join(SAMPLE_DIR, "inputs")
SAMPLE_OUTPUTS = os.path.join(SAMPLE_DIR, 'outputs')
RESOURCES = os.path.join(BASE_DIR, "resources")

#PRAW CREDENTIALS

CLIENT_ID = ""
CLIENT_SECRET = ""
USERNAME = ""
PASSWORD = ""
USER_AGENT = ""

#GOOGLE CREDENTIALS

CREDENTIALS = os.path.join(BASE_DIR, "") #Gcloud project credentials json file goes here