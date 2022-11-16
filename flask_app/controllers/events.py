from flask_app import app
from flask_app.models import event,user
from flask import request, redirect,render_template,session,flash

@app.route('/dashboard')
def logged():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html',events=event.Event.show_all_event(),user=user.User.get_by_id(session['user_id']))
@app.route('/create_event')
def create_event():
    return render_template('create_event.html',user=user.User.get_by_id(session['user_id']))
@app.route("/edit/<int:id>")
def edit_event(id):
    return render_template('edit_event.html',user=user.User.get_by_id(session['user_id']),event=event.Event.by_id(id))
@app.route('/delete/<int:id>')
def delete(id):
    event.Event.destroy(id)
    return redirect('/dashboard')  
@app.route("/view/<int:id>")
def view(id):
    return render_template('view_event.html',event=event.Event.by_id(id),user=user.User.get_by_id(session['user_id']),skeptics=user.User.skeptic(id))




@app.route('/create',methods=['POST'])
def save():
    valid=event.Event.save_event(request.form)
    if not valid:
        return redirect('/create_event')
    return redirect('/dashboard')
@app.route('/edit/event/<int:id>',methods=['POST'])
def update(id):
    valid=event.Event.update_event(request.form)
    print(valid)
    if valid==False:
        return redirect(f'/edit/{id}')
    return redirect('/dashboard') 
@app.route('/believe/<int:id>',methods=['POST']) 
def believer(id):
    data={
        'user_id':request.form['user_id'],
        'event_id':request.form['event_id']
    }
    event.Event.believer(data)
    return redirect(f'/view/{id}')
@app.route("/skeptic/<int:id>", methods=['POST'])
def skeptic(id):  
    data={
        'user_id':request.form['user_id']
    }  
    event.Event.skeptic(data)
    return redirect(f'/view/{id}')
