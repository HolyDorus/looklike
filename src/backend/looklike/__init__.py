# Load .env file
from dotenv import load_dotenv
load_dotenv()


from flask import Flask
from .settings import settings


app = Flask(__name__)
app.config.from_object(settings)
