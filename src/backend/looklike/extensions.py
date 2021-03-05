from flask_cors import CORS

from looklike.configs import config


cors = CORS(resources={r'/*': {'origins': config.FRONTEND_URL}})
