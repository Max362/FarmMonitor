from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

#Defining a blueprint
views = Blueprint('views', __name__)

#Defining route for home page
@views.route('/', methods=['GET', 'POST'])
#We cannot get to the home page unless we login first
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            #Here we are adding note
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    #current_user detects if user is logged in or not
    return render_template("home.html", user=current_user)

#Defining route for delete note
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    #get is accessing the primary key in the database
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/terms')
def terms():
    return render_template("terms.html")

@views.route('/privacy')
def privacy():
    return render_template("privacy.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")
