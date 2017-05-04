from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,login_required,fresh_login_required,logout_user,current_user
from forms import LoginForm,SignupForm,AddProjectForm
from models import User,Project
from . import app,db,bcrypt

@app.route('/')#{{{
def index():
    return render_template('index.html')
#}}}
@app.route('/signup/',methods=['GET','POST'])#{{{
def signup():
    form=SignupForm()
    if form.validate_on_submit():
        email,username=form.email.data,form.username.data
        if not User.query.filter(db.or_(User.email==email,User.username==username)).first():#try unique=True in models
            password_hash=bcrypt.generate_password_hash(form.password.data)
            new_user=User(email=email,username=username,password=password_hash,admin=False)
            if not User.query.first():
                new_user.admin=True
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)#,remember=form.remember.data)
            return redirect(url_for('projects_list'))
        flash('Email or username already taken, please try again')
        return redirect(url_for('signup'))
    return render_template('signup.html',form=form)
#}}}
@app.route('/login/',methods=['GET','POST'])#{{{
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username,password=form.username.data,form.password.data
        user=User.query.filter(User.username==username).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)#,remember=form.remember.data)
            flash('Welcome, '+current_user.username)
            return redirect(url_for('projects_list'))
        flash('Username or password incorrect, please try again')
        return redirect(url_for('login'))
    return render_template('login.html',form=form)
#}}}
@app.route('/logout/')#{{{
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('index'))
#}}}
@app.route('/projects_list/',methods=['GET','POST'])#{{{
@login_required
def projects_list():
    projects=Project.query.all()
    return render_template('projects_list.html',projects=projects)
#}}}
@app.route('/delete_project/',methods=['POST'])#{{{
@fresh_login_required
def delete_project():
    if not current_user.admin:
        flash('Admin rights required')
        return redirect(url_for('index'))
    project=Project.query.get(request.form['project_id'])
    if project.user_id:
        User.query.get(project.user_id).project_id=0
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted')
    return redirect(url_for('projects_list'))
#}}}
@app.route('/select_project/',methods=['POST'])#{{{
@login_required
def select_project():
    if current_user.admin:
        flash('Forbidden request')
        return redirect(url_for('projects_list'))
    project=Project.query.get(request.form['project_id'])
    project.user_id=current_user.id
    current_user.project_id=project.id
    db.session.commit()
    flash('Project selected')
    return redirect(url_for('projects_list'))
#}}}
@app.route('/leave_project/',methods=['POST'])#{{{
@login_required
def leave_project():
    if current_user.admin:
        flash('Forbidden request')
        return redirect(url_for('projects_list'))
    Project.query.get(current_user.project_id).user_id=0
    current_user.project_id=0
    db.session.commit()
    flash('Project left')
    return redirect(url_for('projects_list'))
#}}}
@app.route('/free_project/',methods=['POST'])#{{{
@fresh_login_required
def free_project():
    project=Project.query.get(request.form['project_id'])
    User.query.get(project.user_id).project_id=0
    project.user_id=0
    db.session.commit()
    flash('Project available')
    return redirect(url_for('projects_list'))
#}}}
@app.route('/add_project/',methods=['GET','POST'])#{{{
@fresh_login_required
def add_project():
    if not current_user.admin:
        flash('Admin rights required')
        return redirect(url_for('index'))
    form=AddProjectForm()
    if form.validate_on_submit():
        project=Project(title=form.title.data,text=form.text.data)
        db.session.add(project)
        db.session.commit()
        flash('Project added')
        return redirect(url_for('projects_list'))
    return render_template('add_project.html',form=form)
#}}}
@app.route('/users_list/',methods=['GET','POST'])#{{{
@login_required
def users_list():
    if not current_user.admin:
        flash('Admin rights required')
        return redirect(url_for('index'))
    users=User.query.all()
    return render_template('users_list.html',users=users)
#}}}
@app.route('/delete_user/',methods=['POST'])#{{{
@fresh_login_required
def delete_user():
    if not current_user.admin:
        flash('Admin rights required')
        return redirect(url_for('index'))
    user=User.query.get(request.form['user_id'])
    if user.project_id:
        Project.query.get(user.project_id).user_id=0
    db.session.delete(user)
    db.session.commit()
    flash('User deleted')
    return redirect(url_for('users_list'))
#}}}
@app.route('/reset_all/')#{{{
@fresh_login_required
def reset_all():
    if not current_user.admin:
        flash('Admin rights required')
        return redirect(url_for('index'))
    all_users=User.query.all()
    all_projects=Project.query.all()
    flash(str(len(all_users))+' user(s) and '+str(len(all_projects))+' project(s) deleted.')
    for item in all_users+all_projects:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))
#}}}
@app.route('/make_admin/',methods=['POST'])#{{{
@fresh_login_required
def make_admin():
    if not current_user.admin:
        flash('Admin rights required')
        return redirect(url_for('index'))
    user=User.query.get(request.form['user_id'])
    user.admin=True
    db.session.commit()
    flash('Admin rights granted to '+user.username)
    return redirect(url_for('users_list'))
#}}}
@app.route('/make_normal_user/',methods=['POST'])#{{{
@fresh_login_required
def make_normal_user():
    if not current_user.admin:
        flash('Admin rights required')
        return redirect(url_for('index'))
    user=User.query.get(request.form['user_id'])
    user.admin=False
    db.session.commit()
    flash(user.username+' lost admin rights')
    return redirect(url_for('users_list'))
#}}}
#select project with project_id, free project with user_id
#"admin_required" with flask-login
#precise flash error msg (email must be email, etc)
