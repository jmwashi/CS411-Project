from app import app
import requests
from flask import render_template, flash, redirect,url_for , Flask
from app.forms import SearchForm,SearchEventForm

#from eventbrite import Eventbrite
import requests
import json
import pytz, datetime

def local_to_utc(time):
    local = pytz.timezone("America/Los_Angeles")
    naive = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.strftime ("%Y-%m-%dT%H:%M:%SZ")

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        headers = {'Authorization': 'Bearer xbpwPL_a5NvDdKSqQzZNY-6vSGJWS_6VgQgy0-ZtXg1jMvj3_bmniqTd5dZLJ2We2kRqcdS9XjywXXOkcpk-Dr89tQ4Y6GAlDOMfILJgCyvb3lNR5fZvmO8v2lvOW3Yx'}
        params = {'location': form.city.data,
          'term': form.keyword.data,
          'sort_by': 'rating',
          'limit': form.numberOfRestaruants.data
         }
        result = requests.get('https://api.yelp.com/v3/businesses/search',headers=headers,params=params,verify=False)
        output = result.json()
        output = output["businesses"]
        finalString=[]
        for counter in range (int(params['limit'])):
            location = output[counter]["location"]
            location = location["city"]
            outputString={"Name":output[counter]["name"],"Location":location,"Picture":output[counter]["image_url"],"Rating":str(output[counter]["rating"])}
            finalString.append(outputString)
        return render_template("response.html",title='Title',result=finalString)
    return render_template('index.html', title='Title', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_event():
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
    result=requests.get("https://www.eventbriteapi.com/v3/events/search/?"+search_string+"&token=SYL7IV644GMFGG7FON47")
    result=result.json()
    display_string=[]
    for event in result["events"]:

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
            
    return render_template("eventbrite.html", form=form, result=display_string)
  return render_template("eventbriteform.html",form=form)

#@app.route('/result')
#def result():

#    return result
