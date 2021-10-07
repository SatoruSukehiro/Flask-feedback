"""Basic Flask app ready to connect to database"""
from flask import Flask,render_template,request,session,flash
from flask.helpers import flash
from flask.json import jsonify
from flask_bcrypt import Bcrypt
from werkzeug.utils import redirect
from models import connect_db,db,User,Feedback
from form import RegisterUser,Login,FeedbackForm


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ITSASECRETDUHHH"

connect_db(app)
bcrypt = Bcrypt()

 #route           
@app.route('/')
def homepage():
    return redirect('/login')


@app.route('/register',methods=["GET","POST"])
def register_user():
    form = RegisterUser()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name=form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username=username,
                                 password=password,
                                 email=email,
                                 first_name=first_name,last_name=last_name)
        session["username"] = username
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users/{username}')
    else: 
        return render_template('register_form.html',form=form)


@app.route('/login', methods=["GET","POST"])
def login_user():
    form = Login()
    
    if "username" in session:
        return redirect(f'users/{session["username"]}')
    
    if form.validate_on_submit():
        username= form.username.data
        password = form.password.data
        
        user = User.verify(username,password)
        if user:
             session["username"] = username
             return redirect(f'/users/{username}')
        else:   
            form.username.errors=["The Username/Password you tried was incorrect please try again"]
            return render_template('/login.html',form=form)
    else:
        return render_template('/login.html',form=form)




@app.route('/users/<username>')
def get_secret(username):
    user= User.query.filter_by(username=username).first()
    form= Login()
    if "username" not in session or session['username'] != username:
        
        flash("YOU MUST BE LOGGED IN")     
        return redirect('/login')
        
    else:
        if session["username"] == username:
            return render_template("secret.html",user=user)

@app.route('/users/<username>/delete')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user or session["username"] != user.username:
        flash('MUST BE LOGGED IN TO DELETE')
        return redirect('/')
    else:
        db.session.delete(user)
        db.session.commit()
        session.clear()
        return redirect('/')




@app.route('/users/<username>/feedback/add',methods=["GET","POST"])
def add_user_feedback(username):
    form = FeedbackForm() 
    title = form.title.data
    content = form.content.data
    if form.validate_on_submit():
        new_feedback = Feedback(title=title,content=content,username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('/feedback.html',form=form)


@app.route('/feedback/<int:id>/update',methods=["GET","POST"])
def update_feedback(id):
    feedback = Feedback.query.get(id)
    form= FeedbackForm(obj=feedback)
    
    if "username" not in session or session["username"] != feedback.user.username:
        return redirect('/login')

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    
    return render_template('/feedback.html',form=form)


@app.route('/feedback/<int:id>/delete', methods=["GET"])
def delete_feedback(id):
    feedback = Feedback.query.get(id)
    username = feedback.user.username
    db.session.delete(feedback)
    db.session.commit()
    
    if "username" not in session or session["username"] !=  feedback.user.username:
        flash('YOU CANT DO THAT ')
        return redirect('/login')
    
    return redirect(f'/users/{username}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    