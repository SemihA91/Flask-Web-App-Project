from selenium.webdriver import Chrome, ChromeOptions
from flask_app import create_app
import multiprocessing
import pytest
import os


@pytest.fixture(scope="module")
def test_client():
    """
    Yields a test client with an empty database
    """

    try:
        os.remove('flask_app/test.db')
    except FileNotFoundError:
        pass

    app = create_app(test=True)

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def test_client_with_user(test_client):
    """
    Yields a test client with a single test user
    """

    details = {
        'username': 'human42',
        'first name': 'Hugh',
        'last name': 'Mann',
        'email': 'human42@gmail.com',
        'password': 'strongpassword',
        'confirm password': 'strongpassword'
    }

    test_client.post('/signup', data=details)
    test_client.post(
        '/login',
        data={
            'email': details['email'],
            'password': details['password']
        }
    )

    yield test_client


@pytest.fixture(scope="module")
def test_client_with_blog_post(test_client_with_user):
    """
    Yields a test client with a single blog post
    """

    test_client_with_user.post(
        '/blog/new',
        data={
            'title': 'First Post',
            'post': 'Hello world!'
        },
        follow_redirects=True
    )

    yield test_client_with_user


@pytest.fixture(scope='module')
def chrome_driver():
    """
    Selenium webdriver with options to support running in GitHub actions
    """
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    chrome_driver = Chrome(options=options)
    yield chrome_driver
    chrome_driver.close()


@pytest.fixture(scope='module')
def run_app():
    """
    Fixture to run the Flask app for Selenium browser tests
    """
    app = create_app(test=True)
    multiprocessing.set_start_method("fork")
    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()
