from environ import Env
from pathlib import Path

from dotenv import load_dotenv

# -------------------------------------------------------------------------------------------------------------------- #
# Get .env variables                                                                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
load_dotenv()
env = Env()

TOKEN = env("TG_TOKEN")
ADMINS = tuple(map(int, env("ADMIN_IDS").split()))
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Make directories and defaults                                                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR/"file_store"
# -------------------------------------------------------------------------------------------------------------------- #
