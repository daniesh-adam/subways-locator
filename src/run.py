from app import create_app


# Explicitly import configuration so that PyInstaller is able to find
# and bundle it
import config

application = create_app("config.ProductionConfig")

if __name__ == "__main__":
    application.run(debug=False)
