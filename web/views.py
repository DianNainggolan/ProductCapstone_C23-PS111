from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Diary
from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        diary = request.form.get('diary')

        if len(diary) < 1:
            flash('Your Diary is too short!', category='error') 
        else:
            new_diary = Diary(data=diary, user_id=current_user.id)  
            db.session.add(new_diary) 
            db.session.commit()
            flash('Diary added!', category='success')

    return render_template("home.html", user=current_user)

