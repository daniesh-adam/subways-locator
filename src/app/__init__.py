import os
import sys
from flask import Flask


def get_root_dir_abs_path() -> str:
    """Get the absolute path to the root directory of the application."""
    # Check if the application runs in a bundled executable from PyInstaller.
    # When executed, the bundled executable get's upacked into the temporary directory
    # See also: https://pyinstaller.org/en/stable/runtime-information.html#using-file
    return getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))


def create_app() -> Flask:
    """
    Initialise Flask app.

    Args:
        config_object_name (object): The python path of the config object.

    Returns:
        Flask: Flask app
    """
    root_dir_abs_path = get_root_dir_abs_path()

    # Initialise the core application
    app = Flask(__name__,
                instance_relative_config=False,
                static_folder=os.path.join(root_dir_abs_path, "static"),
                template_folder=os.path.join(root_dir_abs_path, "templates")
                )

    # if not config_object_name is None:
    # app.config.from_object("config.ProductionConfig")
    app.config['DEBUG'] = False
    app.config['FIREWORKS_API_KEY'] = 'SqBWv34DVdUJFGpIWO6IXvgDzCpeHvjMXcsRm6IIJScUGOHx'
    app.config['DB_PATH'] = 'app/data/outlets.db'

    with app.app_context():
        from app import views
        return app


application = create_app()
