from app import app
from app import db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, MeetUpCreateForm,EventCreateForm,SearchForm,SelectForm,SearchEventForm,EBForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User,Event,Meet
from flask import request
from werkzeug.urls import url_parse
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session
from oauth import OAuthSignIn
import requests
import json
import pytz, datetime

yelpDict = {}
ebDict = {}
result = ''

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


@app.route('/search_yelp/<meet_id>',methods=['GET','POST'])
def searchYelp(meet_id):
    form = SearchForm()
    if form.validate_on_submit():
        headers = {'Authorization': 'Bearer xbpwPL_a5NvDdKSqQzZNY-6vSGJWS_6VgQgy0-ZtXg1jMvj3_bmniqTd5dZLJ2We2kRqcdS9XjywXXOkcpk-Dr89tQ4Y6GAlDOMfILJgCyvb3lNR5fZvmO8v2lvOW3Yx'}
        params = {'location': form.city.data,
          'term': form.keyword.data,
          'sort_by': 'rating',
          'limit': form.numberOfRestaruants.data
        }
        result = requests.get('https://api.yelp.com/v3/businesses/search',headers=headers,params=params,verify=False)
        yelpResults = result.json()
        session['params'] = params
        session['yelpResults'] = yelpResults
        return redirect(url_for('yelp_create',meet_id=meet_id))
    return render_template('searchYelp.html', title='Title', form=form)

@app.route('/create_yelp/<meet_id>', methods=['GET', 'POST'])
def yelp_create(meet_id):
    form = SelectForm()
    params = session.get('params')
    yelpResults = session.get('yelpResults', None)
    yelpResults = yelpResults["businesses"]
    finalString=[]
    ourchoices = []
    count = 1
    for counter in range (int(params['limit'])):
        location = yelpResults[counter]["location"]
        location = location["city"]
        outputString={"Name":yelpResults[counter]["name"],"Location":location,"Picture":yelpResults[counter]["image_url"],"Rating":str(yelpResults[counter]["rating"])}
        finalString.append(outputString)
        thisString = 'Option '+str(count)
        thisTuple = (thisString,yelpResults[counter]["name"])
        yelpDict[thisString] = count
        ourchoices.append(thisTuple)
        count += 1
    form.selection.choices = ourchoices
    if form.validate_on_submit():
        index = yelpDict[form.selection.data]-1
        location = yelpResults[counter]["location"]
        city = location["city"]
        address = location["address1"]
        event = Event(title = yelpResults[index]["name"],this_id=meet_id, description = "Restaurant", address = address, city = city,time = 'N/A')
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('meetups'))
    return render_template('response.html', result=finalString,title='Title', form=form)
    
def local_to_utc(time):
    local = pytz.timezone("America/New_York")
    naive = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.strftime ("%Y-%m-%dT%H:%M:%SZ")

@app.route('/search_eventbrite/<meet_id>', methods=['GET', 'POST'])
def search_eventbrite(meet_id):
  form = SearchEventForm()
  if form.validate_on_submit():
    # input 
    params={
        "q": form.keyword.data,
        "sort_by":form.sort_by.data,
        "location.address":form.location.data,
        "location.within": str(form.location_within.data)+"km",
        "price":form.price.data,
        "start_date.range_start":local_to_utc(form.start_after.data),
        "start_date.range_end": local_to_utc(form.start_before.data),
        #"start_date.keyword":""
    }
    search_string=""
    for param in params:
        search_string+=str(param)+"="+str(params[param])+"&"

    # parse the result
    global result
    result=requests.get("https://www.eventbriteapi.com/v3/events/search/?"+search_string+"&token=SYL7IV644GMFGG7FON47")
    result=result.json()
    #print(result)
    return redirect(url_for('eventbrite',meet_id=meet_id))
  return render_template("eventbriteform.html",form=form)

@app.route('/create_eventbrite/<meet_id>', methods=['GET', 'POST'])
def eventbrite(meet_id):
    global result
    form = EBForm()
    print(result)
    display_string=[]
    ourchoices = []
    count = 1
    for event in result["events"]:
        thisString = 'Option '+str(count)
        thisTuple = (thisString,event["name"]["text"])
        ebDict[thisString] = count
        ourchoices.append(thisTuple)
        new_event={"name":event["name"]["text"],
             "description":event["description"]["text"],
             "id":event["id"],
             "start_time":event["start"]["local"],
             "end_time":event["end"]["local"],
             "online":event["online_event"],
             "is_free":event["is_free"],
             "logo":"",
             "url":event["url"]
             }

        if event["logo"] is not None:
           new_event["logo"]=event["logo"]["url"]
    
        display_string.append(new_event)
        count += 1
    form.selection.choices = ourchoices   
    if form.validate_on_submit():
        index = ebDict[form.selection.data]-1
        event = Event(title = result["events"][index]["name"]["text"],this_id=meet_id, description = result["events"][index]["url"], address = "",city = "",time = result["events"][index]["start"]["local"])
        db.session.add(event)
        db.session.commit()
        print(result["events"][index]["name"]["text"])
    return render_template("eventbrite.html", form=form, result=display_string)