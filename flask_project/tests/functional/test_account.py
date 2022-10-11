def test_user_navbar(test_client_with_user):
    """
    GIVEN an app instance where a user is logged in
    WHEN the user goes to the homepage
    THEN profile and logout buttons are present in the navbar
    """

    resp = test_client_with_user.post('/', follow_redirects=True)

    assert resp.status_code == 200
    assert b'Profile' in resp.data
    assert b'Logout' in resp.data


def test_user_about_me(test_client_with_user):
    """
    GIVEN an app instance where a user is logged in
    WHEN changes their "About Me"
    THEN the profile shows their new "About Me"
    """

    resp = test_client_with_user.post(
        '/profile/human42',
        data={'about-text': 'I like to do human things'},
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b'I like to do human things' in resp.data


def test_user_logout(test_client_with_user):
    """
    GIVEN an app instance where a user is logged in
    WHEN the user logs out
    THEN profile and logout buttons are not present in the navbar
    """

    resp = test_client_with_user.open('/logout', follow_redirects=True)

    assert resp.status_code == 200
    assert b'Profile' not in resp.data
    assert b'Logout' not in resp.data


def test_user_profile_logged_out(test_client_with_user):
    """
    GIVEN an app instance where a user is logged out
    WHEN the user tries to view their profile
    THEN the user is redirected to the login page
    """

    resp = test_client_with_user.open(
        '/profile/human42',
        follow_redirects=False
    )

    assert resp.status_code == 302
    assert '/login' in resp.location
