from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc

from models import db
from forms import EventCreateForm, LoginForm, RegisterForm
from models import login_manager, Event, User
from util import admin_required

blueprint_base = Blueprint('base', __name__, template_folder='templates')
blueprint_users = Blueprint('users', __name__, template_folder='templates')
blueprint_events = Blueprint('events', __name__, template_folder='templates')


@blueprint_base.route("/")
def index():
    return render_template("base/index.html")


@blueprint_base.app_errorhandler(404)
def error_404(e):
    return render_template('base/404.html'), 404

@blueprint_users.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        login_user(login_form.get_user())
        return redirect(
            url_for('.profile'))  # TODO: implement safe redirection based on url value for login and register
    return render_template('users/login.html', login_form=login_form)


login_manager.login_view = '/login'


@blueprint_users.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = User(email=register_form.email.data,
                        username=register_form.username.data,
                        password=register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('.profile'))
    return render_template('users/register.html', register_form=register_form)


@blueprint_users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base.index'))


@blueprint_users.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('users/profile.html')


@blueprint_events.route('/create', methods=['GET', 'POST'])
@login_required
def events_create():
    event_create_form = EventCreateForm()
    if event_create_form.validate_on_submit():
        new_event = Event(owner=current_user,
                          title=event_create_form.title.data,
                          start_time=event_create_form.start_time.data,
                          duration=event_create_form.duration.data,
                          description=event_create_form.description.data,
                          link=event_create_form.link.data)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('.events_list'))
    return render_template('events/create.html', event_create_form=event_create_form)


@blueprint_events.route('/')
def events_list():
    events = Event.query.filter_by(approved=True).order_by(desc(Event.start_time)).all()
    return render_template('events/list.html', events=events)


@blueprint_events.route('/unapproved')
@admin_required
def events_unapproved():
    unapproved_events = Event.query.filter_by(approved=False).order_by(desc(Event.start_time)).all()
    return render_template('events/list.html', events=unapproved_events, enabled_actions=['approve'])


@blueprint_events.route('/<int:event_id>/approve', methods=['POST'])
@admin_required
def events_approve(event_id):
    event = Event.query.get_or_404(event_id)
    if event.approved:
        flash("Event %d already approved!" % event_id)
    else:
        event.approved = True
        db.session.commit()
        flash("Event %d approved!" % event_id)
    return redirect(url_for('.events_unapproved'))