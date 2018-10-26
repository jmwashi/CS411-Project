from app import app
import requests
from flask import render_template, flash, redirect
from app.forms import SearchForm

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


#@app.route('/result')
#def result():

#    return result
