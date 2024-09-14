from flask import render_template, request, redirect, url_for
from app import app, db
from models import User, Task, Project

# Home route
@app.route('/')
def home():
    return "Welcome to the Task Management System!"

# User route (list users)
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Create new user
@app.route('/user/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name, email=email, password=password, role='Member')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('new_user.html')

# Project route (list projects)
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

# Task route (list tasks)
@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# Add new task
@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title=title, description=description, priority='Medium', status='Pending')
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('new_task.html')
