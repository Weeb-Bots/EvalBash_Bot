import os
import dotenv


if os.path.exists(".env"):
  dotenv.load_dotenv()

class Config(object):
  CHAT_ID = os.environ.get("CHAT_ID", "")
  USERS = os.environ.get("AUTH_USERS", "5375981312 5152550390 5126929234") # Me, Sinner, Dark
  BOT_TOKEN = os.environ.get("BOT_TOKEN")
  TGID = int(os.environ.get("API_ID"))
  TGHASH = os.environ.get("API_HASH")
