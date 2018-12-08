from app import app
from app import db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, MeetUpCreateForm,EventCreateForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User,Event,Meet
from flask import request
from werkzeug.urls import url_parse
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session
from oauth import OAuthSignIn



@app.route('/')
@app.route('/index')
@app.route('/profile')
def index():
    if current_user.is_anonymous:
        return redirect('/authorize/facebook')
    return render_template("index.html", title='Home Page')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#need to call database to grab current user to properly create event and meetup. doing tonight
@app.route('/create_event/<meet_id>',methods=['GET', 'POST'])
@login_required
def createEvent(meet_id):
    form = EventCreateForm()
    if form.validate_on_submit():
        event = Event(title = form.title.data,this_id=meet_id, description = form.description.data, address = form.address.data, city = form.city.data,time = form.time.data)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('meetups'))
    return render_template('createEvent.html',form=form)

@app.route('/meet/<meet_id>',methods=['GET','POST'])
@login_required
def thisMeet(meet_id):
    user = User.query.filter_by(id=current_user.id).first_or_404()
    meet = Meet.query.filter_by(id=meet_id).first_or_404()
    events = Event.query.filter_by(this_id=meet.id).all()
    return render_template('thisMeet.html',user=user,meet=meet,events=events)


@app.route('/create_meetup',methods=['GET', 'POST'])
@login_required
def createMeetUp():
    form = MeetUpCreateForm()
    if form.validate_on_submit():
        meet_up = Meet(title = form.title.data,owner_id = current_user.id, description = form.description.data, city = form.city.data)
        db.session.add(meet_up)
        db.session.commit()
        return redirect(url_for('meetups'))
    return render_template('createMeetUp.html',form=form)

@app.route('/meetups')
@login_required
def meetups():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    meet_ups = Meet.query.filter_by(owner_id=current_user.id).all()
    return render_template('meetups.html',user=user,meet_ups=meet_ups)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        print('test')
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))
