from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from user import User
from time import Time
from user import setUserToDb
from user import getUserFromDb
from user import search
add = Blueprint('add', __name__)


@add.route('/timeline/add', methods=['GET', 'POST'])
def add_new_time_info():
    if request.method == 'GET':
        form = { 'decade': '', 'year': '', 'share_date':'', 'content_type':'', 'content_header':''}
        timeline = current_app.timesql.get_timeinfo()
        return render_template('index.html', timeline=timeline, form=form)
    else:
        decade_temp = request.form['decade']
        year_temp = request.form['year']
        share_date_temp = request.form['share_date']
        content_type_temp = request.form['content_type']
        content_header_temp = request.form['content_header']
        timeinfo_temp = Event( decade=decade_temp, year=year_temp,share_date= share_date_temp,content_type= content_type_temp,content_header= content_header_temp)
        current_app.timesql.add_timeinfo(timeinfo_temp)
        timeline = current_app.timesql.get_timeinfo()
        form = { 'decade': '', 'year': '', 'share_date':'', 'content_type':'', 'content_header':''}
        return render_template('index.html', timeline=timeline, form = form)

@add.route('/timeline/delete', methods=['GET', 'POST'])
def delete_timeinfo():
    if request.method == 'GET':
        timeline = current_app.timesql.get_timeinfo()
        form = { 'decade': '', 'year': '', 'share_date':'', 'content_type':'', 'content_header':''}
        return render_template('index.html', timeline=timeline, form = form)
    else:
        map_id_list = request.form.getlist('map_id_list')
        for map_id in map_id_list:
            current_app.timesql.delete_timeinfo(varchar(map_id))
        timeline = current_app.timesql.get_timeinfo()
        form = { 'decade': '', 'year': '', 'share_date':'', 'content_type':'', 'content_header':''}
        return render_template('index.html', timeline=timeline, form = form)





@add.route('/events/documents/update/<int:event_id>', methods=['GET', 'POST'])
def update_time_info(event_id):
    if request.method == 'GET':
        time = current_app.timesql.get_time(event_id)
        form = { 'decade': time.decade, 'year': time.year, 'share_date':time.share_date, 'content_type':time.content_type, 'content_header':time.content_header}
        return render_template('update_index.html',  form = form)

    else:
        decade_temp = request.form['decade']
        year_temp = request.form['year']
        share_date_temp = request.form['share_date']
        content_type_temp = request.form['content_type']
        content_header_temp = request.form['content_header']
        timeinfo_temp = Event( decade=decade_temp, year=year_temp,share_date= share_date_temp,content_type= content_type_temp,content_header= content_header_temp)
        current_app.timesql.update_timeinfo(timeinfo_temp,map_id)
        current_app.timesql.add_timeinfo(timeinfo_temp)
        timeline = current_app.timesql.get_timeinfo()
        form = { 'decade': '', 'year': '', 'share_date':'', 'content_type':'', 'content_header':''}
        return render_template('index.html', timeline=timeline, form = form)



