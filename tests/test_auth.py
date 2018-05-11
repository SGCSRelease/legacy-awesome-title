# Third Party
import pytest

# Local Application
from AwesomeTitleServer import auth


def test_login(client, auth):
    # test that viewing the page renders without template errors
    assert client.get('/auth/login').status_code == 200

    # test that successful login redirects to the index page
    assert response.headers['Location'] == 'https://localhost/'

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get('/')
        assert session['username'] == 'test'


def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get('/auth/register').status_code == 200

    # test that successful registration redirects to the login page
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.header['Location']

    # test that the user was inserted into the database
    with app.app_context():
        assert User.query.filter(
            User.username == 'a'
        ).first() is not None
