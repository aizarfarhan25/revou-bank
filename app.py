from config.setting import create_app
from utils.database import db  # noqa: F401

app = create_app("config.local")

