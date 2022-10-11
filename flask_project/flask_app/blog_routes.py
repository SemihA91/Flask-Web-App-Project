from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import ForumPost
from . import db

blog = Blueprint('blog', __name__)


@blog.route("/blog/new")
@login_required
def make_post():

    """
    Route to make a new post page.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'make_post.html' page

    """

    return render_template('make_post.html', title='New Post')


@blog.route("/blog/new", methods=['POST'])
def post_made():

    """
    Route for the new post function. Gets user input and inserts it into
    the database

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        redirects user to the blog.start_blog page

    """

    # Getting the information from the form
    title = request.form.get('title')
    post = request.form.get('post')

    newPost = ForumPost(title=title, post=post, poster=current_user)
    db.session.add(newPost)
    db.session.commit()

    flash(f'{"{Post Added}"}', "success")
    return redirect(url_for('blog.start_blog'))


@blog.route('/blog/oldest')
def start_blog():

    """
    Route which orders the blog posts oldest first

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'blog.html' page

    """

    posts = ForumPost.query.all()

    return render_template('blog.html', title='blog', posts=posts)


@blog.route('/blog/newest')
def reverse_blog():

    """
    Route which orders the blog posts newest first

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'blog.html' page

    """

    posts = ForumPost.query.all()
    posts.reverse()
    return render_template('blog.html', title='blog', posts=posts)


@blog.route("/blog/<post_id>")
def post_id(post_id):

    """
    Used to expand a single post with more information

    Parameters
    ----------
    post_id : Integer
        Id of the post in the database

    Returns
    -------
    render_template() : Function
        Renders the 'single_post.html' page including the parameters for the
        post title(title), post contents(contents) and the users profile
        picture(avatar)

    """

    post = ForumPost.query.get_or_404(post_id)
    return render_template('single_post.html', title=post.title, post=post,
                           avatar=post.poster.avatar)


@blog.route('/blog/delete_post/<post_id>')
@login_required
def delete_post(post_id):

    """
    Route for the delete post function. Allows the
    creator to delete the selected post

    Parameters
    ----------
    post_id : Integer
        Id of the post in the database

    Returns
    -------
    redirect() : Function
        redirects user to the blog.start_blog page

    """

    post = ForumPost.query.get_or_404(post_id)
    if post.poster.username == current_user.username:
        ForumPost.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(url_for('blog.start_blog'))
