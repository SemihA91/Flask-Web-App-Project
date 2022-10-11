from time import sleep
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures('chrome_driver', 'run_app')
def test_app_runs_in_browser(chrome_driver):
    """
    GIVEN the app is running
    WHEN the app is openend in a browser
    THEN the heading title should be displayed
    """

    sleep(3)
    chrome_driver.get('http://127.0.0.1:5000/')
    assert chrome_driver.title == 'Volcano and meteorite blog'


@pytest.mark.usefixtures('chrome_driver', 'run_app')
def test_browser_blog(chrome_driver):
    """
    GIVEN the app is running in a browser
    WHEN the Blog button is clicked on
    THEN the page is redirected to the blog page
    """

    sleep(3)

    chrome_driver.get('http://127.0.0.1:5000/')
    chrome_driver.implicitly_wait(3)
    chrome_driver.find_element(By.LINK_TEXT, "Blog").click()
    chrome_driver.implicitly_wait(3)

    heading = chrome_driver.find_element(By.ID, 'heading').text

    assert 'General Volcano/Meteor Blog' in heading


@pytest.mark.usefixtures('chrome_driver', 'test_client')
def test_browser_signup_success(chrome_driver):
    """
    GIVEN the app is running in a browser
    WHEN a user signs up
    THEN the user is redirected to the login page
    """

    sleep(3)

    chrome_driver.get('http://127.0.0.1:5000/')
    chrome_driver.implicitly_wait(3)
    chrome_driver.find_element(By.LINK_TEXT, "Sign up").click()
    chrome_driver.implicitly_wait(3)

    chrome_driver.find_element(By.ID, "inputUsername").send_keys("thelegend27")
    chrome_driver.find_element(By.ID, "inputFirstName").send_keys("Dave")
    chrome_driver.find_element(By.ID, "inputLastName").send_keys("Davey")
    chrome_driver.find_element(By.ID, "inputEmail").send_keys("legend@mail.fr")
    chrome_driver.find_element(By.ID, "inputPassword").send_keys("27")
    chrome_driver.find_element(By.ID, "confirmPassword").send_keys("27")

    chrome_driver.find_element(By.ID, "register").click()
    chrome_driver.implicitly_wait(3)

    assert '/login' in chrome_driver.current_url


@pytest.mark.usefixtures('chrome_driver', 'test_client')
def test_browser_login_failure(chrome_driver):
    """
    GIVEN the app is running in a browser and a
    user account has been created
    WHEN the user logs in with the incorrect details
    THEN the user is redirected back to the login page
    """

    sleep(3)

    chrome_driver.get('http://127.0.0.1:5000/')
    chrome_driver.implicitly_wait(3)
    chrome_driver.find_element(By.LINK_TEXT, "Login").click()
    chrome_driver.implicitly_wait(3)

    chrome_driver.find_element(By.ID, "inputEmail").send_keys("legend@mail.fr")
    chrome_driver.find_element(By.ID, "inputPassword").send_keys("wrongpass")

    chrome_driver.find_element(By.ID, "loginbutton").click()
    chrome_driver.implicitly_wait(3)

    assert '/login' in chrome_driver.current_url


@pytest.mark.usefixtures('chrome_driver', 'test_client')
def test_browser_login_success(chrome_driver):
    """
    GIVEN the app is running in a browser and a
    user account has been created
    WHEN the user logs in with the correct details
    THEN the user is redirected to the homepage
    """

    sleep(3)

    chrome_driver.get('http://127.0.0.1:5000/')
    chrome_driver.implicitly_wait(3)
    chrome_driver.find_element(By.LINK_TEXT, "Login").click()
    chrome_driver.implicitly_wait(3)

    chrome_driver.find_element(By.ID, "inputEmail").send_keys("legend@mail.fr")
    chrome_driver.find_element(By.ID, "inputPassword").send_keys("27")

    chrome_driver.find_element(By.ID, "loginbutton").click()
    chrome_driver.implicitly_wait(3)

    assert '/' in chrome_driver.current_url
