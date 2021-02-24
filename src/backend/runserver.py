from looklike import create_app
from looklike.configs import config


if __name__ == "__main__":
    app = create_app(config)
    app.run()
