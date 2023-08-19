import os

from dotenv import load_dotenv
from flask_migrate import Migrate


load_dotenv()

from app_utils import create_app

DEBUG = os.environ.get('DEBUG') == 'TRUE' or False
basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app(__name__)


from models import db, User, Merchant
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Merchant': Merchant}


if __name__ == '__main__':
    app.run()
