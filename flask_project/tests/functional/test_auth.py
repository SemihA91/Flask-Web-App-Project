def test_signup_success(test_client):
    """
    GIVEN an app instance
    WHEN a valid form is submitted to /signup
    THEN redirect to /login
    """

    resp = test_client.post(
        '/signup',
        data={
            'username': 'human42',
            'first name': 'Hugh',
            'last name': 'Mann',
            'email': 'human42@gmail.com',
            'password': 'strongpassword',
            'confirm password': 'strongpassword'
        },
        follow_redirects=False
    )

    assert resp.status_code == 302
    assert resp.location == '/login'


def test_signup_already_exists(test_client):
    """
    GIVEN an app instance
    WHEN a form is submitted to /signup with an existing user
    THEN redirect back to /signup and prompt user exists error
    """

    resp = test_client.post(
        '/signup',
        data={
            'username': 'human42',
            'first name': 'Hugh',
            'last name': 'Mann',
            'email': 'human42@gmail.com',
            'password': 'strongpassword',
            'confirm password': 'strongpassword'
        },
        follow_redirects=True
    )

    # Test if redirect was successful
    assert resp.status_code == 200

    # Test if page is /signup
    assert b'<form method = "POST" action="/signup">' in resp.data

    # Test if existing details prompt is shown
    assert b'already in use' in resp.data


def test_signup_mismatch_passwords(test_client):
    """
    GIVEN an app instance
    WHEN a form is submitted to /signup with mismatching passwords
    THEN redirect back to /signup and prompt mismatch error
    """

    resp = test_client.post(
        '/signup',
        data={
            'username': 'obama',
            'first name': 'Obama',
            'last name': 'Unknown',
            'email': 'obama@gmail.com',
            'password': 'strongpassword',
            'confirm password': 'wrongpassword'
        },
        follow_redirects=True
    )

    # Test if redirect was successful
    assert resp.status_code == 200

    # Test if page is /signup
    assert b'<form method = "POST" action="/signup">' in resp.data

    # Test if password mismatch prompt is shown
    assert b'Passwords don&#39;t match' in resp.data


def test_login_success(test_client):
    """
    GIVEN an app instance
    WHEN valid details are provided to /login
    THEN redirect to homepage
    """

    resp = test_client.post(
        '/login',
        data={
            'email': 'human42@gmail.com',
            'password': 'strongpassword'
        },
        follow_redirects=False
    )

    assert resp.status_code == 302
    assert resp.location == '/'


def test_login_failure(test_client):
    """
    GIVEN an app instance
    WHEN invalid details are provided to /login
    THEN redirect back to /login and show error prompt
    """

    resp = test_client.post(
        '/login',
        data={
            'email': 'invalidemail@gmail.com',
            'password': 'invalidpassword'
        },
        follow_redirects=True
    )

    # Test if redirect was successful
    assert resp.status_code == 200

    # Test if page is /login
    assert b'<form method = "POST" action="/login">' in resp.data

    # Test if incorrect login details prompt is shown
    assert b'Please check your login details' in resp.data


def test_password_reset(test_client):
    """
    GIVEN an app instance with a user
    WHEN the password is reset
    THEN the user can login with the new password
    """

    test_client.post('/login', follow_redirects=True)

    test_client.post(
        '/forgot_password',
        data={'email': 'human42@gmail.com'},
        follow_redirects=True
    )

    test_client.post(
        '/reset',
        data={
            'password': '123',
            'confirm_password': '123'
        },
        follow_redirects=True
    )

    resp = test_client.post(
        '/login',
        data={
            'email': 'human42@gmail.com',
            'password': '123'
        },
        follow_redirects=False
    )

    assert resp.status_code == 302
    assert resp.location == '/'
