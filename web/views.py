from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required,  current_user
from .models import Note
from . import db
import json


views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash("Nota es muy corta", category='error')
        else:
            nueva_nota = Note(data=note,user_id=current_user.id)
            db.session.add(nueva_nota)
            db.session.commit()
            flash("Nota agregada", category='success')
    return render_template("home.html",user=current_user)


@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteID']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})