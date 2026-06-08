from dotenv import load_dotenv

load_dotenv()
import pytest
from app import create_app, db as _db

@pytest.fixture(scope="session")
def app():
    flask_app = create_app("testing")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["TESTING"]          = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()

@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    yield
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
