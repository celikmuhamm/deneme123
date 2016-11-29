import os
import base64

from flask import Blueprint, render_template,session,request,flash,Flask
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from user import User
from event import Event, Image
from user import setUserToDb
from user import getUserFromDb
from user import search
from werkzeug.utils import secure_filename

image = Blueprint('image', __name__)

@image.route('/events/images/images_add/add', methods=['GET', 'POST'])
def add_new_image_page():
    if request.method == 'GET':
        return render_template('add_images.html')    
    else:
        image_file = request.files.get('upload')
        content = image_file.read()
        filetype = image_file.content_type
        encoded = base64.b64encode(content)
        encoded_str=encoded.decode("utf-8")
        output = 'data:' + filetype + ';base64,' + encoded_str
        now = datetime.now()
        date = now.strftime('%x')
        event_id = request.form['country']
        event_id = int(event_id)
        image_id = current_app.store_images.get_image_id(event_id) + 1
        image = Image(content=output, event_id=event_id , image_id = image_id, date=date)
        current_app.store_images.add_image(image)
        images = current_app.store_images.get_images(event_id)
        return render_template('images_all.html',images = images, event_id = event_id)

@image.route('/events/images/delete', methods=['GET', 'POST'])
def delete_image():
    if request.method == 'POST':
        image_id_list = request.form.getlist('image_id_list')
        event_id = request.form['delete']
        event_id = int(event_id)
        for image_id in image_id_list:
            current_app.store_images.delete_image(int(image_id), int(event_id))
        images=current_app.store_images.get_images(int(event_id))
        count=1
        if images:
            for image in images:
                if image.image_id != count:
                    current_app.store_images.update_image_id(int(image.image_id), int(event_id),count)
                count += 1
                
        images = current_app.store_images.get_images(event_id)
        return render_template('images_all.html', images=images, event_id = event_id)



