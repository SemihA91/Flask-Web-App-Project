from flask import Blueprint, render_template, request, flash, url_for, redirect

from flask_app.models import ForumPost, User
from . import db
from flask_login import login_required, current_user
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():

    """
    Route for the home page. Either the default advert or uploaded advert
    is displayed.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'home.html' page
    """

    if os.path.exists(os.path.join('flask_app/static/images/',
                      "uploadedad.png")):
        advertisement = "../static/images/uploadedad.png"
    else:
        advertisement = "../static/images/ad.png"
    return render_template('home.html', advertisement=advertisement)


@main.route('/delete')
def delete_ad():
    """
    Route for deleting the advert. if an ad is available it is deleted,
    otherwise an error is flashed.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        redirects user to the main.index page

    """

    if current_user.username == "admin":
        if os.path.exists(os.path.join('flask_app/static/images/',
                                       "uploadedad.png")):
            os.remove(os.path.join('flask_app/static/images/',
                                   'uploadedad.png'))
            return redirect(url_for('main.index'))
        else:
            flash(f'{"There is no ad to delete"}', "error")
            return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@main.route('/', methods=['POST'])
def post_ad():

    """
    Route for posting a new advert. Saves an uploaded image with the name
    uploadedadpng. If an advert already exists it will simply be ovewritten.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        Redirects user to the main.index page

    """

    if request.files:
        image = request.files['image']
        if image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image.filename
            image.save(os.path.join('flask_app/static/images/',
                                    "uploadedad.png"))
        return redirect(url_for('main.index'))

    return redirect(url_for('main.index'))


@main.route('/profile/<username>')
@login_required
def profile(username):

    """
    Route for the profile page which posts the users own created posts to
    their page.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'profile.html' page with the variables username, email,
        about, profile picture, and the users posts.
    """

    user = User.query.filter_by(username=username).first_or_404()
    username = user.username
    posts = ForumPost.query.all()
    posts.reverse()
    return (
        render_template('profile.html', name=username, email=user.email,
                        about=user.about, avatar=user.avatar,
                        user=user, posts=posts)
    )


@main.route('/profile/<username>', methods=['POST'])
@login_required
def get_profile_info(username):

    """
    Route for the profile page which sets the user information
    eg. profile picture,


    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        redirects user to the main.profile route

    """

    user = User.query.filter_by(username=username).first_or_404()
    username = user.username

    if request.files:
        image = request.files['image']
        if image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image.save(os.path.join('flask_app/static/images/',
                                    image.filename))
            current_user.avatar = '../static/images/' + image.filename
            db.session.commit()
        return redirect(url_for('main.profile', username=username))

    current_user.about = request.form.get('about-text')
    db.session.commit()
    return redirect(url_for('main.profile', username=username))
