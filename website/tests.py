from flask import url_for
import pytest
from website import create_app


class TestPage(object):
    def test_home_page(self, client):
        """ Home page should respond with a success 200. """
        response = client.get(url_for('/'))
        assert response.status_code == 200

    def test_login_page(self, client):
        """ Terms page should respond with a success 200. """
        response = client.get(url_for('/login'))
        assert response.status_code == 200

    def test_logout_page(self, client):
        """ Privacy page should respond with a success 200. """
        response = client.get(url_for('/logout'))
        assert response.status_code == 200

    def test_signup_page(self, client):
        """ Privacy page should respond with a success 200. """
        response = client.get(url_for('/sign-up'))
        assert response.status_code == 200

    def test_privacy_page(self, client):
        """ Privacy page should respond with a success 200. """
        response = client.get(url_for('views.privacy'))
        assert response.status_code == 200

    def test_terms_page(self, client):
        """ Privacy page should respond with a success 200. """
        response = client.get(url_for('views.terms'))
        assert response.status_code == 200

    def test_contact_page(self, client):
        """ Privacy page should respond with a success 200. """
        response = client.get(url_for('views.contact'))
        assert response.status_code == 200


#session will save computing, power by running only once at the beginning of test suite
@pytest.fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """
    #params = {
    #    'DEBUG': False,
     #   'TESTING': True
    #}

    _app = create_app()

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()

#function will make sure the tests are independend of each other
@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()