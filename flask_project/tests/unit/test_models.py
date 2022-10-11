from flask_app.models import User, ForumPost


def test_new_user_details_correct():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, email,
    and password fields are defined correctly
    """

    user = User(username="human42",
                first_name="Hugh",
                last_name="Mann",
                email="human42@earthmail.com",
                password="123")

    assert user.username == "human42"
    assert user.first_name == 'Hugh'
    assert user.last_name == 'Mann'
    assert user.email == 'human42@earthmail.com'
    assert user.password == '123'
    assert user.password != 'abc'


def test_new_forum_post_content_correct():
    """
    GIVEN a ForumPost model
    WHEN a new ForumPost is created
    THEN check the id, title, post, date and id_user are correct
    """

    user = User(username="human42",
                first_name="Hugh",
                last_name="Mann",
                email="human42@earthmail.com",
                password="123")

    forum_post = ForumPost(title="Hello World",
                           post="This is a post!",
                           poster=user)

    assert forum_post.title == "Hello World"
    assert forum_post.post != "Some other content."
    assert forum_post.id_user == user.id
