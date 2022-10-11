def test_create_blog_post(test_client_with_user):
    """
    GIVEN an app instance where a user is logged in
    WHEN the user creates a new blog post
    THEN the blog post is shown in the blog tab
    """

    resp = test_client_with_user.post(
        '/blog/new',
        data={
            'title': 'First Post',
            'post': 'Hello world!'
        },
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b'First Post' in resp.data
    assert b'Hello world!' in resp.data
    assert b'By human42' in resp.data


def test_delete_blog_post(test_client_with_user):
    """
    GIVEN an app instance where a user is logged in
    and a blog post has been created
    WHEN the user deletes a blog post
    THEN the blog post is no longer in the blog tab
    """

    resp = test_client_with_user.open(
        '/blog/delete_post/1',
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b'First Post' not in resp.data
    assert b'Hello world!' not in resp.data
    assert b'By human42' not in resp.data


def test_delete_blog_post_logged_out(test_client_with_blog_post):
    """
    GIVEN an app instance where a user is logged out
    WHEN the user goes to a blog post
    THEN then the option to delete the post is absent
    """

    test_client_with_blog_post.open(
        '/logout', follow_redirects=True)

    resp = test_client_with_blog_post.open(
        '/blog/1',
        follow_redirects=False
    )

    assert resp.status_code == 200
    assert b'Delete Post' not in resp.data
