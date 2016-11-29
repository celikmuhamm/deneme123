from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from user import User
from event import Event, Document
from user import setUserToDb
from user import getUserFromDb
from user import search
add = Blueprint('add', __name__)


@add.route('/events/documents/add', methods=['GET', 'POST'])
def add_new_document_page():
    if request.method == 'GET':
        form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
        events = current_app.store.get_events()
        return render_template('documents.html', events=events, form=form)    
    else:
        title_temp = request.form['inputTitle']
        date_temp = request.form['inputDate']
        id_temp = request.form['event_number']
        content_temp = request.form['comment']
        document_id = current_app.store_documents.get_document_id(id_temp) + 1
        document_temp = Document(title = title_temp, date=date_temp, event_id=id_temp,content= content_temp, document_id = document_id)
        current_app.store_documents.add_document(document_temp)
        documents = current_app.store_documents.get_documents(id_temp)
        return render_template('documents.html', documents=documents)
    
@add.route('/events/documents/delete', methods=['GET', 'POST'])
def delete_document():
    if request.method == 'POST':
        document_id_list = request.form.getlist('document_id_list')
        event_id = request.form['delete']
        for document_id in document_id_list:
            current_app.store_documents.delete_document(int(document_id), int(event_id))
        documents=current_app.store_documents.get_documents(int(event_id))
        count=1
        if documents:
            for document in documents:
                if document.document_id != count:
                    current_app.store_documents.update_document_id(int(document.document_id), int(event_id),count)
                count += 1
        
        
        
        documents = current_app.store_documents.get_documents(event_id)
        return render_template('documents.html', documents=documents)


   
    
@add.route('/events/documents/update/<int:event_id>/<int:document_id>', methods=['GET', 'POST'])
def update_documents_page(document_id, event_id):
    if request.method == 'GET':
        document = current_app.store_documents.get_document(document_id, event_id)
        event = current_app.store.get_event(int(document.event_id))
        event=event[0]
        events = current_app.store.get_events()
        form = {'inputTitle': document.title, 'inputDate': document.date, 'comment':document.content}
        return render_template('update_documents.html', events=events, form=form)  
                               
    else:
        title_temp = request.form['inputTitle']
        date_temp = request.form['inputDate']
        content_temp = request.form['comment']
        document_temp = Document(title = title_temp, date=date_temp, event_id=event_id,content= content_temp, document_id = document_id)
        current_app.store_documents.update_document(document_temp,event_id,document_id)
        documents = current_app.store_documents.get_documents(event_id)
        return render_template('documents.html', documents=documents)
    
    

   