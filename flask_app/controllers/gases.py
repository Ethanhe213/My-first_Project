from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user,gas
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html',gas=gas.Gas.show_all(),user=user.User.get_by_id(session['user_id']))
@app.route('/create_gas')
def create_gas():
    return render_template('create_gas.html')
@app.route('/create',methods=['POST'])
def create():
    valid=gas.Gas.save_gas(request.form)
    if not valid:
        return redirect('/create_gas')
    return redirect('/dashboard')